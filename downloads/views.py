
from experiments.models import Experiment
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from .export import create_directory, ExportExecution
from .input_export import build_complete_export_structure
from .models import Export

from os import path
from shutil import rmtree
from zipfile import ZipFile

JSON_FILENAME = "json_export.json"
JSON_EXPERIMENT_FILENAME = "json_experiment_export.json"
EXPORT_DIRECTORY = "temp"
DOWNLOAD_DIRECTORY = "download"
EXPORT_FILENAME = "download.zip"
EXPORT_EXPERIMENT_FILENAME = "download_experiment.zip"


# Create your views here.
def create_export_instance():
    export_instance = Export()

    export_instance.save()

    return export_instance


def download_view(request, experiment_id):
    template_name = "experiments/detail.html"

    complete_filename, error_msg = download_create(experiment_id, template_name)

    if error_msg != "":
        messages.error(request, error_msg)
        return render(request, template_name)

    if complete_filename:

        messages.success(request, "Download was finished correctly")

        # print("antes do fim: httpResponse")
        #
        zip_file = open(complete_filename, 'rb')
        response = HttpResponse(zip_file, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="export.zip"'
        response['Content-Length'] = path.getsize(complete_filename)
        response['Set-Cookie'] = 'fileDownload=true; path=/'
        return response
    else:
        messages.error(request, "Download data was not generated.")

    return HttpResponseRedirect(template_name)


def get_export_instance(export_id):
    export_instance = Export.objects.get(id=export_id)

    return export_instance


def update_export_instance(input_file, output_export, export_instance):
    export_instance.input_file = input_file
    export_instance.output_export = output_export
    export_instance.save()


def download_create(experiment_id, template_name):
    try:
        export_instance = create_export_instance()
        input_export_file = path.join(EXPORT_DIRECTORY,
                                      path.join(path.join(str(export_instance.id), str(JSON_FILENAME))))
        input_filename = path.join(settings.MEDIA_ROOT, input_export_file)

        create_directory(settings.MEDIA_ROOT, path.split(input_export_file)[0])

        build_complete_export_structure(experiment_id, input_filename)

        export = ExportExecution(export_instance.id)

        # set path of the directory base: ex. /Users/.../portal/media/temp/
        base_directory, path_to_create = path.split(export.get_directory_base())
        # create directory base ex. /Users/.../portal/media/temp/path_create
        error_msg, base_directory_name = create_directory(base_directory, path_to_create)

        # ex. /Users/.../portal/media/temp/export_instance.id/json_export.json
        input_export_file = path.join("export", path.join(path.join(str(export_instance.id), str(input_filename))))

        # prepare data to be processed
        input_data = export.read_configuration_data(input_filename)

        if not export.is_input_data_consistent() or not input_data:
            error_msg = "Inconsistent data read from json file"

        # create directory base for export: /EXPERIMENT_DOWNLOAD
        error_msg = export.create_export_directory()

        # load information of the data collection per participant in a dictionnary
        error_msg = export.include_data_from_group(experiment_id)

        # Create arquivos para exportação
        # create files of experimental protocol and diagnosis/participant csv file for each group
        error_msg = export.process_experiment_data(experiment_id)

        # process the data per participant
        error_msg = export.download_data_per_participant()

        # process the data per questionnaire
        error_msg = export.download_data_per_questionnaire()

        # create zip file and include files
        export_complete_filename = ""
        if export.files_to_zip_list:
            export_filename = export.get_input_data("export_filename")  # 'download.zip'

            export_complete_filename = path.join(base_directory_name, export_filename)
            directory_download_base = path.join(settings.MEDIA_ROOT, "download")

            download_experiment_directory = path.join(directory_download_base, str(experiment_id))

            if not path.exists(download_experiment_directory):
                error_msg, download_experiment_directory = create_directory(directory_download_base, str(experiment_id))

            download_complete_filename = path.join(download_experiment_directory, export_filename)

            with ZipFile(export_complete_filename, 'w') as zip_file:
                for filename, directory in export.files_to_zip_list:
                    fdir, fname = path.split(filename)

                    zip_file.write(filename.encode('utf-8'), path.join(directory, fname))

            zip_file.close()

            output_download_file = path.join("download", path.join(path.join(str(experiment_id), str(export_filename))))

            with open(export_complete_filename, 'rb') as f:
                data = f.read()

            with open(download_complete_filename, 'wb') as f:
                f.write(data)

            # experimento ultima versão
            experiment = get_object_or_404(Experiment, pk=experiment_id)
            experiment.download_url = "download/" + str(experiment_id) + "/" + export_filename
            experiment.save(update_fields=["download_url"])

            update_export_instance(input_export_file, output_download_file, export_instance)

        # delete temporary directory: from base_directory and below
        base_export_directory = path.join(settings.MEDIA_ROOT, path.join("temp", str(export_instance.id)))
        rmtree(base_export_directory, ignore_errors=True)

        if template_name != "":
            return download_complete_filename, error_msg

    except OSError as e:
        print(e)
        error_msg = e
        # messages.error(request, error_msg)
        # return render(request, template_name)
        if template_name != "":
            return error_msg

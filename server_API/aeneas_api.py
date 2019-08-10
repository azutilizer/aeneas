#!/usr/bin/env python
# coding=utf-8

from aeneas.exacttiming import TimeValue
from aeneas.executetask import ExecuteTask
from aeneas.language import Language
from aeneas.syncmap import SyncMapFormat
from aeneas.task import Task
from aeneas.task import TaskConfiguration
from aeneas.textfile import TextFileFormat
import aeneas.globalconstants as gc

# create Task object
config = TaskConfiguration()
config[gc.PPN_TASK_LANGUAGE] = Language.ENG
config[gc.PPN_TASK_IS_TEXT_FILE_FORMAT] = TextFileFormat.PLAIN
config[gc.PPN_TASK_OS_FILE_FORMAT] = SyncMapFormat.JSON
task = Task()
task.configuration = config


def get_align(audio_file, text_file):
    task.audio_file_path_absolute = audio_file
    task.text_file_path_absolute = text_file

    # process Task
    ExecuteTask(task).execute()

    # print produced sync map
    result = {'result': []}
    for fragment in task.sync_map_leaves():
        if fragment.text == '':
            continue
        text = fragment.text
        st_time = fragment.pretty_print.split('\t')[1]
        ed_time = fragment.pretty_print.split('\t')[2]
        result['result'].append({'sentence': text, 'time': [float(st_time), float(ed_time)]})
        print('{:50s} => {}'.format(fragment.text, fragment.interval))

    return result

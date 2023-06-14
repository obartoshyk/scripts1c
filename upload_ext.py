#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''Upload external report from xml'''
from utils_1c import argparse_1c, settings_1c
from utils_1c import basedata, connection_1c
from utils_1c import ocv8


class ReportUploader(object):
    def __init__(self, parser_obj):
        super(ReportUploader, self).__init__()
        self.parser = parser_obj
        self.ds_base = basedata.get_designer_base(**self.parser.get_single_base_params())
        self.xml = parser_obj.args["xml"][0]
        self.ext = "/tmp/ext_re{}.tmp".format(settings_1c.str_cur_time_str())
        print(parser_obj.args["xml"][0])

    def upload(self):
        with connection_1c.Connection(srv=self.parser.args["server"][0], **self.parser.args) as conn:
            dc = ocv8.DesignerCommand(*[],
                                      cmd_func=conn.cast,
                                      env="DISPLAY=:1")
            dc.LoadExternalDataProcessorOrReportFromFiles(self.xml, self.ext)


def init_main():
    parser = argparse_1c.ArgumentParser_1C("sBudkf", description=__doc__)
    parser.add_argument('-X', '--xml',
                        metavar="xml",
                        help='xml root file',
                        nargs="*", type=str, required=True)
    parser.decode_arg()
    return parser


if __name__ == "__main__":
    ReportUploader(init_main()).upload()

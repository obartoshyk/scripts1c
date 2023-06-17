#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''Upload external report from xml'''
from utils_1c import argparse_1c, settings_1c
from utils_1c import basedata, connection_1c
from utils_1c import ocv8


class PluginConverter(object):
    def __init__(self, parser_obj):
        super(PluginConverter, self).__init__()
        self.parser = parser_obj
        self.ds_base = basedata.get_designer_base(**self.parser.get_single_base_params())
        self.xml = parser_obj.args["xml"][0]
        self.ext = "/home/baal/Desktop/test1/ext_re{}.erf".format(settings_1c.str_cur_time_str())
        self.log = "/tmp/PluginConverter_{}.txt".format(settings_1c.str_cur_time_str())
        self.env = parser_obj.args["env"][0]

    def upload(self):
        with connection_1c.Connection(srv=self.parser.args["server"][0], **self.parser.args) as conn:
            dc = ocv8.DesignerCommand(*self.ds_base.getparams(),
                                      cmd_func=conn.cast,
                                      env=self.env)
            dc.LoadExternalDataProcessorOrReportFromFiles(self.xml, self.ext, self.log)


def arg_parser_main():
    parser = argparse_1c.ArgumentParser_1C("sBudkf", description=__doc__)
    parser.add_argument('-x', '--xml',
                        metavar="xml",
                        help='xml root file',
                        nargs="*", type=str, required=True)
    parser.decode_arg()
    print(parser.args)
    return parser


if __name__ == "__main__":
    arg_parser_main()
    #PluginConverter(arg_parser_main()).upload()

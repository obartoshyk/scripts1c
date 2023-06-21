#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''Upload external report from xml'''
from utils_1c import argparse_1c, settings_1c
from utils_1c import basedata, connection_1c, rep
from utils_1c import ocv8


class PluginConverter(object):
    def __init__(self, dc):
        super(PluginConverter, self).__init__()
        self.dc = dc

    def convert(self, xml_to_ext, ext_to_xml):
        log = "/tmp/PluginConverter_{}.txt".format(settings_1c.str_cur_time_str())
        for xml, ext in xml_to_ext:
            self.dc.LoadExternalDataProcessorOrReportFromFiles(xml, ext, log)
        for xml, ext in ext_to_xml:
            self.dc.DumpExternalDataProcessorOrReportToFiles(xml, ext, log)


def arg_parser_main():
    parser = argparse_1c.ArgumentParser_1C("sBudkf", description=__doc__)
    parser.decode_arg()
    return parser


if __name__ == "__main__":
    parser = arg_parser_main()
    ds_base = basedata.get_designer_base(**parser.get_single_base_params())
    with connection_1c.Connection(srv=parser.args["server"][0], **parser.args) as conn:
        dc = ocv8.DesignerCommand(*ds_base.getparams(),
                                  cmd_func=conn.cast,
                                  env=parser.args["env"][0])
        cl = rep.RepositoryPlugins(parser, conn).get_pl_files_list()

        #PluginConverter(dc).convert(*cl)



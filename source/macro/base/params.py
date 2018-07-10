# encoding: utf-8


'''
author: Taehong Kim
email: peppy0510@hotmail.com
'''


class Params():

    def __init__(self, staff_size=None, staves_size=None, systems_size=None,
                 page_margin=14, page_extra_spaces=3, auto_breaks_bars=None,
                 show_instrument_name=None, instrument_staff_margin=None, instrument_name_barline_gap=None):

        self.staff_size = staff_size
        self.staves_size = staves_size
        self.systems_size = systems_size
        self.staff_margin = systems_size
        self.page_margin = page_margin
        self.page_extra_spaces = page_extra_spaces
        self.auto_breaks_bars = auto_breaks_bars
        self.show_instrument_name = show_instrument_name
        self.instrument_staff_margin = instrument_staff_margin
        self.instrument_name_barline_gap = instrument_name_barline_gap

        # if None not in (self.staff_size, self.instrument_names_spaces):
        #     names_margin = int(self.staff_size * 1.9 + self.instrument_names_spaces - 2)
        #     self.instrument_fullnames_margin = names_margin
        #     self.instrument_shortnames_margin = names_margin
        #     self.instrument_nonames_margin = 0

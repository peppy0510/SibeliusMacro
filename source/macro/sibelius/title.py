# encoding: utf-8


'''
author: Taehong Kim
email: peppy0510@hotmail.com
'''


import base


class RemoveTitle(base.MacroBase):

    name = 'Remove Title'

    def run(self):

        modal = self._get_position_title_modal_()
        title_margin = modal.key.get_text()
        modal.key.bulk(['100{TAB}100'])
        modal.key.bulk(['{ENTER}'])

        modal = self._get_position_composer_modal_()
        composer_margin = modal.key.get_text()
        # modal.key.bulk(['{TAB}'])
        # modal.key.get_text()
        modal.key.bulk(['100{TAB}100'])
        modal.key.bulk(['{ENTER}'])

        self.root.key.menu(['{ALT}|V|PV'])
        modal = self._get_documentsetup_top_margin_modal_()
        modal.key.bulk(['{ALT}M{TAB}{TAB}'])
        page_width = float(modal.key.get_text())
        modal.key.bulk(['{ALT}M' + '{TAB}' * 9])
        prev_top_margin = modal.key.get_text()
        modal.key.bulk(['%0.2f' % (page_width + 15)])
        modal.key.bulk(['{ENTER}'])
        self.root.key.menu(['{ALT}|V|ZM|PW'])
        self.root.key.bulk(['{CTRL}{HOME}|{CTRL}{PAGEUP}'])

        score = base.Control(self.root).get('WindowControl', name='Score')
        rect = score.get_rect()
        pos = self.mouse.get_position()

        margin = 1
        x = rect.x + margin
        y = rect.y + margin
        self.mouse.move(x, y)
        self.root.key.down('{SHIFT}')
        self.mouse.down(x, y)
        x = x + rect.width - margin * 2 - 19
        y = y + rect.width - margin * 2
        self.mouse.move(x, y)
        self.root.key.up(['{SHIFT}|{LSHIFT}|{RSHIFT}'])
        self.wait(50)
        self.mouse.up(x, y)
        self.wait(50)
        self.mouse.move(pos.x, pos.y)
        self.wait(50)
        self.root.key.send(['{DEL}'])

        modal = base.Control(self.root).get('WindowControl', includes=[
            'Deleting this text will remove it from the score and all of your parts.'])
        modal.key.bulk(['N'])
        modal = base.Control(self.root).get('WindowControl', name='Sibelius')
        modal.key.bulk(['{ENTER}'])

        modal = self._get_documentsetup_top_margin_modal_()
        modal.key.bulk(['{ALT}M' + '{TAB}' * 9])
        modal.key.bulk(['%s' % (prev_top_margin)])
        modal.key.bulk(['{ENTER}'])
        self.root.key.menu(['{ALT}|V|FP'])
        self.root.key.bulk(['{CTRL}{HOME}|{CTRL}{PAGEUP}'])

        modal = self._get_position_title_modal_()
        modal.key.bulk(['%s{TAB}%s' % (title_margin, title_margin)])
        modal.key.bulk(['{ENTER}'])

        modal = self._get_position_composer_modal_()
        modal.key.bulk(['%s{TAB}%s' % (composer_margin, composer_margin)])
        modal.key.bulk(['{ENTER}'])

    def _set_layout_(self):
        self.root.key.menu(['{ALT}|V|FP'])
        self.root.key.bulk(['{CTRL}{HOME}|{CTRL}{PAGEUP}'])

    def _get_position_title_modal_(self):
        self.root.key.esc()
        self.root.key.menu(['{ALT}|A|DP'])
        modal = base.Control(self.root).get('WindowControl', name='Default Positions')
        modal.key.bulk(['{TAB}{END}' + '{UP}' * 6])
        modal.key.bulk(['{TAB}' * 5])
        return modal

    def _get_position_composer_modal_(self):
        self.root.key.esc()
        self.root.key.menu(['{ALT}|A|DP'])
        modal = base.Control(self.root).get('WindowControl', name='Default Positions')
        modal.key.bulk(['{TAB}{HOME}' + '{DOWN}' * 15])
        modal.key.bulk(['{TAB}' * 5])
        return modal

    def _get_documentsetup_top_margin_modal_(self):
        self.root.key.esc()
        self.root.key.bulk(['{CTRL}D'])
        # self.root.key.send(['{ALT}|L|DS'])
        modal = base.Control(self.root).get('WindowControl', name='Document Setup')
        # modal.key.bulk(['{ALT}M{TAB}{TAB}{TAB}{TAB}{TAB}{TAB}{TAB}{TAB}{TAB}'])
        return modal

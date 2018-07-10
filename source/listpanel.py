# encoding: utf-8


'''
author: Taehong Kim
email: peppy0510@hotmail.com
'''


import os
import stat
import subprocess
import wx

from ObjectListView import ColumnDefn
from ObjectListView import ObjectListView
from listitem import ObjectItem
from mpath import mpath


class FileDropTarget(wx.FileDropTarget):

    def __init__(self, parent):
        wx.FileDropTarget.__init__(self)
        self.parent = parent

    def OnDropFiles(self, x, y, paths):
        self.StackObjectFiles(paths)
        return 0

    def StackObjectFiles(self, paths):

        extended_paths = list()
        # if self.parent.parent.AutoClearWhenImport.IsChecked():
        #     self.parent.OLV.SetObjects([])
        self.parent.OLV.SetObjects([])

        existing_paths = [v.path for v in self.parent.OLV.GetObjects()]
        for path in paths:
            extended_paths.append(path)
            stats = os.stat(path)
            if stats[stat.ST_MODE] == 16895:  # Folder
                extended_paths += mpath(path).search_subpath()

        for cnt in range(0, len(extended_paths), 2000):
            jobseg = list()
            for path in extended_paths[cnt:cnt + 2000]:
                if path in existing_paths:
                    continue
                existing_paths += [path]
                if os.stat(path)[stat.ST_MODE] == 16895:
                    continue
                jobseg.append(ObjectItem(path))
            self.parent.Freeze()
            self.parent.OLV.AddObjects(jobseg)
            self.parent.Thaw()
        try:
            del extended_paths, stats, jobseg
        except Exception:
            pass
        self.parent.Freeze()
        self.parent.SortList()
        self.parent.Thaw()
        # self.parent.parent.AutoPreview()


class ListPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        # self.OLV = ObjectListView(self, style=wx.LC_REPORT | wx.FLOOD_BORDER)
        self.OLV = ObjectListView(self, style=wx.LC_REPORT | wx.BORDER_DEFAULT)
        self.OLV.SetDropTarget(FileDropTarget(self))
        self.OLV.SetEmptyListMsg('')
        self.OLV.SetEmptyListMsgFont(wx.FFont(10, wx.DEFAULT))
        self.OLV.oddRowsBackColor = (255, 255, 255)
        self.OLV.evenRowsBackColor = (255, 255, 255)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.OLV, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetFilesListColumns()
        self.OLV.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.OLV.Bind(wx.EVT_LIST_BEGIN_DRAG, self.OnDrag)
        self.OLV.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.OLV.Bind(wx.EVT_LEFT_DCLICK, self.OnOpenSelected)
        self.OLV.Bind(wx.EVT_LIST_COL_CLICK, self.OnListColumnClick)

    def SetFilesListColumns(self):
        self.OLV.cellEditMode = ObjectListView.CELLEDIT_F2ONLY
        # Columns = [ColumnDefn(title='IsFile', valueGetter='isfile', valueSetter='isfile',
        #                       isEditable=False, align='left', fixedWidth=0)]
        Columns = [ColumnDefn(title='Status', valueGetter='status', valueSetter='status',
                              isEditable=False, align='center', fixedWidth=80)]
        # Columns += [ColumnDefn(title='Filename', valueGetter='filename', valueSetter='filename',
        #                        isEditable=False, align='left', width=400, minimumWidth=28, maximumWidth=1000)]
        # Columns += [ColumnDefn(title='Directory', valueGetter='directory', valueSetter='directory',
        #                        isEditable=False, align='left', width=290, minimumWidth=28, maximumWidth=1000)]
        Columns += [ColumnDefn(title='Path', valueGetter='path', valueSetter='path',
                               isEditable=False, align='left', width=400, minimumWidth=28, maximumWidth=1000)]
        self.OLV.SetColumns(Columns)
        # self.SortList()

    def OnListColumnClick(self, event):
        pass

    def SortList(self):
        self.parent.Freeze()
        self.Freeze()
        self.OLV.Freeze()
        self.OLV.SortBy(1, ascending=True)
        # for v in dir(self.OLV.innerList):
        #     print v
        # self.OLV.SetTextColour(wx.RED)
        # self.OLV.SortBy(0, ascending=True)
        self.OLV.Thaw()
        self.Thaw()
        self.parent.Thaw()

    def OnKeyDown(self, event):
        keycode = event.GetKeyCode()

        if keycode == 81:  # Q
            self.parent.rotate_script(backward=True)
        if keycode == 87:  # W
            self.parent.rotate_script()
        if keycode == 69:  # E
            pass

        if keycode == wx.WXK_DELETE:
            selected = self.OLV.GetSelectedObjects()
            if len(selected) != 0:
                self.OLV.RemoveObjects(selected)
                self.SortList()
            # self.parent.AutoPreview()
        if keycode == wx.WXK_F5:
            self.parent.OnPreviewButton(None)
        if keycode == wx.WXK_F6:
            self.parent.OnRenameButton(None)
        # event.Skip()

    def OnOpenSelected(self, event):
        selected = self.OLV.GetSelectedObjects()
        if len(selected) == 0:
            return
        command = 'cmd /c START "" "%s"' % (selected[0].path)
        subprocess.call(command)

    def OnRightDown(self, event):
        selected = self.OLV.GetSelectedObjects()
        if len(selected) == 0:
            return
        if len(selected) == 1:
            self.context_menu = ['Open', 'Delete']
        else:
            self.context_menu = ['Delete']
        popupmenu = wx.Menu()
        self.menu_title_by_id = {}
        for idx, title in enumerate(self.context_menu):
            popupmenu.Append(idx, title)
            popupmenu.Bind(wx.EVT_MENU, self.OnContextMenu)
        self.PopupMenu(popupmenu, event.GetPosition())
        popupmenu.Destroy()

    def OnContextMenu(self, event):

        def OnRenameSelected():
            pass

        def OnDeleteSelected():
            selected = self.OLV.GetSelectedObjects()
            self.Freeze()
            self.OLV.RemoveObjects(selected)
            self.SortList()
            self.Thaw()

        operation = self.context_menu[event.GetId()]
        if operation == 'Open':
            self.OnOpenSelected(None)
        if operation == 'Rename':
            OnRenameSelected()
        if operation == 'Delete':
            OnDeleteSelected()

    def OnDrag(self, event):
        return
        selected = self.OLV.GetSelectedObjects()
        data = wx.FileDataObject()
        obj = event.GetEventObject()
        for this in selected:
            data.AddFile(this.path)
        dropSource = wx.DropSource(obj)
        dropSource.SetData(data)
        dropSource.DoDragDrop()

    def OnButtonDeleteAll(self, event):
        selected = self.OLV.GetObjects()
        self.OLV.RemoveObjects(selected)
        event.Skip()

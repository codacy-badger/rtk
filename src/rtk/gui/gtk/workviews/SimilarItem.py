# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.workviews.SimilarItem.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""SimilarItem Work View."""

from pubsub import pub

# Import other RTK modules.
from rtk.gui.gtk import rtk
from rtk.gui.gtk.rtk.Widget import _, gtk
from .WorkView import RTKWorkView


class SimilarItem(RTKWorkView):
    """
    Display Similar Item attribute data in the Work Book.

    The WorkView displays all the attributes for the Failure Mode and Effects
    Analysis (SimilarItem). The attributes of a SimilarItem Work View are:

    :ivar _lst_handler_id: list containing the ID's of the callback signals for
                           each gtk.Widget() associated with an editable
                           Functional SimilarItem attribute.

    +-------+-------------------------------------------+
    | Index | Widget - Signal                           |
    +=======+===========================================+
    |   0   | tvw_similaritem `cursor_changed`          |
    +-------+-------------------------------------------+
    |   1   | tvw_similaritem `button_press_event`      |
    +-------+-------------------------------------------+
    |   2   | tvw_similaritem `edited`                  |
    +-------+-------------------------------------------+
    """

    def __init__(self, controller):
        """
        Initialize the Work View for the Similar Item.

        :param controller: the RTK master data controller instance.
        :type controller: :class:`rtk.RTK.RTK`
        """
        RTKWorkView.__init__(self, controller, module='SimilarItem')

        # Initialize private dictionary attributes.
        self._dic_icons[
            'edit'] = controller.RTK_CONFIGURATION.RTK_ICON_DIR + '/32x32/edit.png'
        self._dic_quality = {
            'Space': 1,
            'Full Military': 2,
            'Ruggedized': 3,
            'Commercial': 4
        }
        self._dic_environment = {
            'Ground, Benign': 1,
            'Ground,Mobile': 2,
            'Naval, Sheltered': 3,
            'Airborne, Inhabited, Cargo': 4,
            'Airborne, Rotary Wing': 5,
            'Space, Flight': 6
        }

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._revision_id = None
        self._parent_id = None
        self._hardware_id = None
        self._method_id = None
        self._dtc_hw_controller = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        _bg_color = '#FFFFFF'
        _fg_color = '#000000'
        _fmt_file = controller.RTK_CONFIGURATION.RTK_CONF_DIR + \
            '/' + controller.RTK_CONFIGURATION.RTK_FORMAT_FILE['similaritem']
        _fmt_path = "/root/tree[@name='SimilarItem']/column"
        _tooltip = _(u"Displays the Similar Item Analysis for the currently "
                     u"selected Hardware item.")

        self.treeview = rtk.RTKTreeView(
            _fmt_path, 0, _fmt_file, _bg_color, _fg_color, pixbuf=False)
        self._lst_col_order = self.treeview.order
        self.treeview.set_tooltip_text(_tooltip)

        self.cmbSimilarItemMethod = rtk.RTKComboBox(
            tooltip=_(u"Select the similar item analysis method."))

        self._lst_handler_id.append(
            self.treeview.connect('cursor_changed', self._do_change_row))
        self._lst_handler_id.append(
            self.treeview.connect('button_press_event', self._on_button_press))
        self._lst_handler_id.append(
            self.cmbSimilarItemMethod.connect('changed',
                                              self._on_combo_changed, 2))

        for _idx in self._lst_col_order[3:]:
            _cell = self.treeview.get_column(
                self._lst_col_order[_idx]).get_cell_renderers()
            try:
                _cell[0].connect('edited', self._do_edit_cell, _idx,
                                 self.treeview.get_model())
            except TypeError:
                _cell[0].connect('toggled', self._do_edit_cell, 'new text',
                                 _idx, self.treeview.get_model())

        _label = rtk.RTKLabel(
            _(u"SimilarItem"),
            height=30,
            width=-1,
            justify=gtk.JUSTIFY_CENTER,
            tooltip=_(u"Displays the Similar Item analysis for the selected "
                      u"hardware item."))
        self.hbx_tab_label.pack_start(_label)

        self.pack_start(self._make_buttonbox(), False, True)
        _hbox = gtk.HBox()
        _hbox.pack_start(self._make_methodbox(), False, True)
        _hbox.pack_end(self._make_treeview(), True, True)
        self.pack_end(_hbox, True, True)
        self.show_all()

        #pub.subscribe(self._do_refresh_view, 'calculatedSimilarItem')
        pub.subscribe(self._on_select_revision, 'selectedRevision')
        pub.subscribe(self._on_select, 'selectedHardware')

    def _do_change_row(self, treeview):
        """
        Handle events for the Similar Item Tree View RTKTreeView().

        This method is called whenever a Tree View row is activated.

        :param treeview: the SimilarItem RTKTreeView().
        :type treeview: :class:`rtk.gui.gtk.rtk.TreeViewRTKTreeView`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        treeview.handler_block(self._lst_handler_id[0])

        _model, _row = treeview.get_selection().get_selected()
        try:
            self._revision_id = _model.get_value(_row, 0)
            self._hardware_id = _model.get_value(_row, 1)
        except TypeError:
            self._revision_id = None
            self._hardware_id = None

        treeview.handler_unblock(self._lst_handler_id[0])

        return _return

    def _do_edit_cell(self, __cell, path, new_text, position, model):
        """
        Handle edits of the Similar Item Work View RTKTreeview().

        :param gtk.CellRenderer __cell: the gtk.CellRenderer() that was edited.
        :param str path: the RTKTreeView() path of the gtk.CellRenderer()
                         that was edited.
        :param str new_text: the new text in the edited gtk.CellRenderer().
        :param int position: the column position of the edited
                             gtk.CellRenderer().
        :param gtk.TreeModel model: the gtk.TreeModel() the gtk.CellRenderer()
                                    belongs to.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        if not self.treeview.do_edit_cell(__cell, path, new_text, position,
                                          model):

            _similaritem = self._dtc_data_controller.request_select(
                self._hardware_id)

            if position == self._lst_col_order[4]:
                _similaritem.quality_from_id = self._dic_quality[model[path][
                    self._lst_col_order[4]]]
            elif position == self._lst_col_order[5]:
                _similaritem.quality_to_id = self._dic_quality[model[path][
                    self._lst_col_order[5]]]
            elif position == self._lst_col_order[6]:
                _similaritem.environment_from_id = self._dic_environment[model[
                    path][self._lst_col_order[6]]]
            elif position == self._lst_col_order[7]:
                _similaritem.environment_to_id = self._dic_environment[model[
                    path][self._lst_col_order[7]]]
            elif position == self._lst_col_order[8]:
                _similaritem.temperature_from = model[path][
                    self._lst_col_order[8]]
            elif position == self._lst_col_order[9]:
                _similaritem.temperature_to = model[path][self._lst_col_order[
                    9]]
            elif position == self._lst_col_order[10]:
                _similaritem.change_description_1 = model[path][
                    self._lst_col_order[10]]
            elif position == self._lst_col_order[11]:
                _similaritem.change_factor_1 = model[path][self._lst_col_order[
                    11]]
            elif position == self._lst_col_order[12]:
                _similaritem.change_description_2 = model[path][
                    self._lst_col_order[12]]
            elif position == self._lst_col_order[13]:
                _similaritem.change_factor_2 = model[path][self._lst_col_order[
                    13]]
            elif position == self._lst_col_order[14]:
                _similaritem.change_description_3 = model[path][
                    self._lst_col_order[14]]
            elif position == self._lst_col_order[15]:
                _similaritem.change_factor_3 = model[path][self._lst_col_order[
                    15]]
            elif position == self._lst_col_order[16]:
                _similaritem.change_description_4 = model[path][
                    self._lst_col_order[16]]
            elif position == self._lst_col_order[17]:
                _similaritem.change_factor_4 = model[path][self._lst_col_order[
                    17]]
            elif position == self._lst_col_order[18]:
                _similaritem.change_description_5 = model[path][
                    self._lst_col_order[18]]
            elif position == self._lst_col_order[19]:
                _similaritem.change_factor_5 = model[path][self._lst_col_order[
                    19]]
            elif position == self._lst_col_order[20]:
                _similaritem.change_description_6 = model[path][
                    self._lst_col_order[20]]
            elif position == self._lst_col_order[21]:
                _similaritem.change_factor_6 = model[path][self._lst_col_order[
                    21]]
            elif position == self._lst_col_order[22]:
                _similaritem.change_description_7 = model[path][
                    self._lst_col_order[22]]
            elif position == self._lst_col_order[23]:
                _similaritem.change_factor_7 = model[path][self._lst_col_order[
                    23]]
            elif position == self._lst_col_order[24]:
                _similaritem.change_description_8 = model[path][
                    self._lst_col_order[24]]
            elif position == self._lst_col_order[25]:
                _similaritem.change_factor_8 = model[path][self._lst_col_order[
                    25]]
            elif position == self._lst_col_order[26]:
                _similaritem.change_description_9 = model[path][
                    self._lst_col_order[26]]
            elif position == self._lst_col_order[27]:
                _similaritem.change_factor_9 = model[path][self._lst_col_order[
                    27]]
            elif position == self._lst_col_order[28]:
                _similaritem.change_description_10 = model[path][
                    self._lst_col_order[28]]
            elif position == self._lst_col_order[29]:
                _similaritem.change_factor_10 = model[path][
                    self._lst_col_order[29]]
            elif position == self._lst_col_order[40]:
                _similaritem.user_blob_1 = model[path][self._lst_col_order[40]]
            elif position == self._lst_col_order[41]:
                _similaritem.user_blob_2 = model[path][self._lst_col_order[41]]
            elif position == self._lst_col_order[42]:
                _similaritem.user_blob_3 = model[path][self._lst_col_order[42]]
            elif position == self._lst_col_order[43]:
                _similaritem.user_blob_4 = model[path][self._lst_col_order[43]]
            elif position == self._lst_col_order[44]:
                _similaritem.user_blob_5 = model[path][self._lst_col_order[44]]
            elif position == self._lst_col_order[45]:
                _similaritem.user_float_1 = model[path][self._lst_col_order[
                    45]]
            elif position == self._lst_col_order[46]:
                _similaritem.user_float_2 = model[path][self._lst_col_order[
                    46]]
            elif position == self._lst_col_order[47]:
                _similaritem.user_float_3 = model[path][self._lst_col_order[
                    47]]
            elif position == self._lst_col_order[48]:
                _similaritem.user_float_4 = model[path][self._lst_col_order[
                    48]]
            elif position == self._lst_col_order[49]:
                _similaritem.user_float_5 = model[path][self._lst_col_order[
                    49]]
            elif position == self._lst_col_order[50]:
                _similaritem.user_int_1 = model[path][self._lst_col_order[50]]
            elif position == self._lst_col_order[51]:
                _similaritem.user_int_2 = model[path][self._lst_col_order[51]]
            elif position == self._lst_col_order[52]:
                _similaritem.user_int_3 = model[path][self._lst_col_order[52]]
            elif position == self._lst_col_order[53]:
                _similaritem.user_int_4 = model[path][self._lst_col_order[53]]
            elif position == self._lst_col_order[54]:
                _similaritem.user_int_5 = model[path][self._lst_col_order[54]]
        else:
            _return = True

        return _return

    def _do_load_tree(self, nodes):
        """
        Iterate through the tree and load the Similar Item RTKTreeView().

        :param nodes: a list of treelib Node()s to load.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _data = []
        _model = self.treeview.get_model()
        _model.clear()

        i = 1
        for _node in nodes:
            _entity = _node.data
            _node_id = _node.identifier

            _assembly = self._dtc_hw_controller.request_get_attributes(
                _node_id)['description']
            _hazard_rate = self._dtc_hw_controller.request_select(
                _node_id, 'reliability').hazard_rate_logistics

            try:
                _quality_from = self._dic_quality.keys()[
                    self._dic_quality.values().index(_entity.quality_from_id)]
            except ValueError:
                _quality_from = ''
            try:
                _quality_to = self._dic_quality.keys()[
                    self._dic_quality.values().index(_entity.quality_to_id)]
            except ValueError:
                _quality_to = ''
            try:
                _environment_from = self._dic_environment.keys()[
                    self._dic_environment.values().index(
                        _entity.environment_from_id)]
            except ValueError:
                _environment_from = ''
            try:
                _environment_to = self._dic_environment.keys()[
                    self._dic_environment.values().index(
                        _entity.environment_to_id)]
            except ValueError:
                _environment_to = ''

            _data = [
                _entity.revision_id, _entity.hardware_id, _assembly,
                _hazard_rate, _quality_from, _quality_to, _environment_from,
                _environment_to, _entity.temperature_from,
                _entity.temperature_to, _entity.change_description_1,
                _entity.change_factor_1, _entity.change_description_2,
                _entity.change_factor_2, _entity.change_description_3,
                _entity.change_factor_3, _entity.change_description_4,
                _entity.change_factor_4, _entity.change_description_5,
                _entity.change_factor_5, _entity.change_description_6,
                _entity.change_factor_6, _entity.change_description_7,
                _entity.change_factor_7, _entity.change_description_8,
                _entity.change_factor_8, _entity.change_description_9,
                _entity.change_factor_9, _entity.change_description_10,
                _entity.change_factor_10, _entity.function_1,
                _entity.function_2, _entity.function_3, _entity.function_4,
                _entity.function_5, _entity.result_1, _entity.result_2,
                _entity.result_3, _entity.result_4, _entity.result_5,
                _entity.user_blob_1, _entity.user_blob_2, _entity.user_blob_3,
                _entity.user_blob_4, _entity.user_blob_5, _entity.user_float_1,
                _entity.user_float_2, _entity.user_float_3,
                _entity.user_float_4, _entity.user_float_5, _entity.user_int_1,
                _entity.user_int_2, _entity.user_int_3, _entity.user_int_4,
                _entity.user_int_5, _entity.parent_id
            ]

            try:
                _row = _model.append(None, _data)
            except TypeError:
                print "FIXME: Handle TypeError in " \
                      "gtk.gui.workviews.SimilarItem.SimilarItem._do_load_tree."
                _return = True
            except ValueError:
                print "FIXME: Handle ValueError in " \
                      "gtk.gui.workviews.SimilarItem.SimilarItem._do_load_tree."
                _return = True
            except AttributeError:
                print "FIXME: Handle AttributeError in " \
                      "gtk.gui.workviews.SimilarItem.SimilarItem._do_load_tree."
                _return = True

            i += 1

        return _return

    def _do_request_calculate(self, __button):
        """
        Request to calculate the Similar Item metrics.

        :param __button: the gtk.ToolButton() that called this method.
        :return: False if sucessful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _model = self.treeview.get_model()
        _row = _model.get_iter_first()

        # Iterate through the hazards and calculate the Similar Item hazard
        # intensities.
        rtk.Widget.set_cursor(self._mdcRTK, gtk.gdk.WATCH)
        while _row is not None:
            _node_id = _model.get_value(_row, 1)
            _hazard_rate = _model.get_value(_row, 3)
            _return = (_return or self._dtc_data_controller.request_calculate(
                _node_id, _hazard_rate))
            _row = _model.iter_next(_row)

        if not _return:
            _nodes = self._dtc_data_controller.request_select_children(
                self._parent_id)
            self._do_load_tree(_nodes)
        rtk.Widget.set_cursor(self._mdcRTK, gtk.gdk.LEFT_PTR)

        return _return

    def _do_request_edit_function(self, __button):
        """
        Request to edit the Similar Item analysis user-defined functions.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        (_model, _row) = self.treeview.get_selection().get_selected()

        _title = _(u"RTK - Edit Similar Item Analysis Functions")
        _label = rtk.RTKLabel(
            _(u"You can define up to five functions.  "
              u"You can use the system failure rate, "
              u"selected assembly failure rate, the "
              u"change factor, the user float, the "
              u"user integer values, and results of "
              u"other functions.\n\n \
        System hazard rate is hr_sys\n \
        Assembly hazard rate is hr\n \
        Change factor is pi[1-8]\n \
        User float is uf[1-3]\n \
        User integer is ui[1-3]\n \
        Function result is res[1-5]"),
            width=600,
            height=-1,
            wrap=True)
        _label2 = rtk.RTKLabel(
            _(u"For example, pi1*pi2+pi3, multiplies "
              u"the first two change factors and "
              u"adds the value to the third change "
              u"factor."),
            width=600,
            height=-1,
            wrap=True)

        # Build the dialog assistant.
        _dialog = rtk.RTKDialog(_title)

        _fixed = gtk.Fixed()

        _y_pos = 10
        _fixed.put(_label, 5, _y_pos)
        _y_pos += _label.size_request()[1] + 10
        _fixed.put(_label2, 5, _y_pos)
        _y_pos += _label2.size_request()[1] + 10

        _label = rtk.RTKLabel(_(u"User function 1:"))
        _txtFunction1 = rtk.RTKEntry()
        _txtFunction1.set_text(_model.get_value(_row, 30))

        _fixed.put(_label, 5, _y_pos)
        _fixed.put(_txtFunction1, 195, _y_pos)
        _y_pos += 30

        _label = rtk.RTKLabel(_(u"User function 2:"))
        _txtFunction2 = rtk.RTKEntry()
        _txtFunction2.set_text(_model.get_value(_row, 31))
        _fixed.put(_label, 5, _y_pos)
        _fixed.put(_txtFunction2, 195, _y_pos)
        _y_pos += 30

        _label = rtk.RTKLabel(_(u"User function 3:"))
        _txtFunction3 = rtk.RTKEntry()
        _txtFunction3.set_text(_model.get_value(_row, 32))
        _fixed.put(_label, 5, _y_pos)
        _fixed.put(_txtFunction3, 195, _y_pos)
        _y_pos += 30

        _label = rtk.RTKLabel(_(u"User function 4:"))
        _txtFunction4 = rtk.RTKEntry()
        _txtFunction4.set_text(_model.get_value(_row, 33))
        _fixed.put(_label, 5, _y_pos)
        _fixed.put(_txtFunction4, 195, _y_pos)
        _y_pos += 30

        _label = rtk.RTKLabel(_(u"User function 5:"))
        _txtFunction5 = rtk.RTKEntry()
        _txtFunction5.set_text(_model.get_value(_row, 34))
        _fixed.put(_label, 5, _y_pos)
        _fixed.put(_txtFunction5, 195, _y_pos)
        _y_pos += 30

        _chkApplyAll = gtk.CheckButton(label=_(u"Apply to all assemblies."))
        _fixed.put(_chkApplyAll, 5, _y_pos)

        _fixed.show_all()

        _dialog.vbox.pack_start(_fixed)  # pylint: disable=E1101

        # Run the dialog and apply the changes if the 'OK' button is pressed.
        if _dialog.run() == gtk.RESPONSE_OK:
            if _chkApplyAll.get_active():
                _row = _model.get_iter_root()
                while _row is not None:
                    _hardware_id = _model.get_value(_row, 1)
                    _similaritem = self._dtc_data_controller.request_select(
                        _hardware_id)
                    _similaritem.function_1 = _txtFunction1.get_text()
                    _similaritem.function_2 = _txtFunction2.get_text()
                    _similaritem.function_3 = _txtFunction3.get_text()
                    _similaritem.function_4 = _txtFunction4.get_text()
                    _similaritem.function_5 = _txtFunction5.get_text()
                    _model.set_value(_row, 30, _similaritem.function_1)
                    _model.set_value(_row, 31, _similaritem.function_2)
                    _model.set_value(_row, 32, _similaritem.function_3)
                    _model.set_value(_row, 33, _similaritem.function_4)
                    _model.set_value(_row, 34, _similaritem.function_5)
                    self._dtc_data_controller.request_update(_hardware_id)
                    _row = _model.iter_next(_row)
            else:
                _similaritem = self._dtc_data_controller.request_select(
                    self._hardware_id)
                _similaritem.function_1 = _txtFunction1.get_text()
                _similaritem.function_2 = _txtFunction2.get_text()
                _similaritem.function_3 = _txtFunction3.get_text()
                _similaritem.function_4 = _txtFunction4.get_text()
                _similaritem.function_5 = _txtFunction5.get_text()
                _model.set_value(_row, 30, _similaritem.function_1)
                _model.set_value(_row, 31, _similaritem.function_2)
                _model.set_value(_row, 32, _similaritem.function_3)
                _model.set_value(_row, 33, _similaritem.function_4)
                _model.set_value(_row, 34, _similaritem.function_5)
                self._dtc_data_controller.request_update(self._hardware_id)

        _dialog.destroy()

        return False

    def _do_request_update(self, __button):
        """
        Request to save the selected Similar Item record.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._dtc_data_controller.request_update(self._hardware_id)

    def _do_request_update_all(self, __button):
        """
        Request to save all the entities in the Similar Item.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._dtc_data_controller.request_update_all()

    def _do_set_visible(self, visible, editable):
        """
        Set the Similar Item treeview columns visible and hidden.

        :param list visible: a list of integers indicating the columns to set
                             visible.
        :param list editable: a list of integers indicating the columns to set
                              editable.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        for _column in self.treeview.get_columns():
            _column.set_visible(0)
        for _col in visible:
            self.treeview.get_column(_col).set_visible(1)
            _column = self.treeview.get_column(_col)
            _cells = _column.get_cell_renderers()
            for __, _cell in enumerate(_cells):
                try:
                    _cell.set_property('background', 'light gray')
                    _cell.set_property('editable', 0)
                except TypeError:
                    _cell.set_property('cell-background', 'light gray')

        for _col in editable:
            _column = self.treeview.get_column(_col)
            _cells = _column.get_cell_renderers()
            for __, _cell in enumerate(_cells):
                try:
                    _cell.set_property('background', 'white')
                    _cell.set_property('editable', 1)
                except TypeError:
                    _cell.set_property('cell-background', 'white')

        return _return

    def _make_buttonbox(self):
        """
        Make the gtk.ButtonBox() for the Similar Item class Work View.

        :return: _buttonbox; the gtk.ButtonBox() for the SimilarItem Work View.
        :rtype: :class:`gtk.ButtonBox`
        """
        _tooltips = [
            _(u"Edit the Similar Item analysis functions."),
            _(u"Calculate the Similar Item analysis."),
            _(u"Save the selected Similar Item analysis to the open RTK "
              u"Program database."),
            _(u"Save all the Similar Item analyses for the selected Hardware "
              u"item to the open RTK Program database.")
        ]
        _callbacks = [
            self._do_request_edit_function, self._do_request_calculate,
            self._do_request_update, self._do_request_update_all
        ]
        _icons = ['edit', 'calculate', 'save', 'save-all']

        _buttonbox = RTKWorkView._make_buttonbox(self, _icons, _tooltips,
                                                 _callbacks, 'vertical')

        return _buttonbox

    def _make_methodbox(self):
        """
        Make the Similar Item analysis method container.

        :return: a gtk.Frame() containing the widgets used to select the
                 allocation method and goals.
        :rtype: :class:`gtk.Frame`
        """
        # Load the method and goal comboboxes.
        self.cmbSimilarItemMethod.do_load_combo([[_(u"Topic 633"), 0],
                                                 [_(u"User-Defined"), 1]])

        _fixed = gtk.Fixed()

        _fixed.put(rtk.RTKLabel(_(u"Select Method")), 5, 5)
        _fixed.put(self.cmbSimilarItemMethod, 5, 30)

        _frame = rtk.RTKFrame(label=_(u"Similar Item Method"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_fixed)

        return _frame

    def _make_treeview(self):
        """
        Make the Similar Item RTKTreeview().

        :return: a gtk.Frame() containing the instance of gtk.Treeview().
        :rtype: :class:`gtk.Frame`
        """
        for _idx in [4, 5]:
            _cell = self.treeview.get_column(
                self._lst_col_order[_idx]).get_cell_renderers()[0]
            _model = _cell.get_property('model')
            for _quality in self._dic_quality:
                _model.append([
                    _quality,
                ])
        for _idx in [6, 7]:
            _cell = self.treeview.get_column(
                self._lst_col_order[_idx]).get_cell_renderers()[0]
            _model = _cell.get_property('model')
            for _environment in self._dic_environment:
                _model.append([
                    _environment,
                ])

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.treeview)

        _frame = rtk.RTKFrame(label=_(u"Similar Item Analysis"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        self.treeview.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

        return _frame

    def _on_button_press(self, treeview, event):
        """
        Handle mouse clicks on the Similar Item Work View RTKTreeView().

        :param treeview: the Similar Item TreeView RTKTreeView().
        :type treeview: :class:`rtk.gui.gtk.rtk.TreeView.RTKTreeView`.
        :param event: the gtk.gdk.Event() that called this method (the
                      important attribute is which mouse button was clicked).

                      * 1 = left
                      * 2 = scrollwheel
                      * 3 = right
                      * 4 = forward
                      * 5 = backwards
                      * 8 =
                      * 9 =

        :type event: :class:`gtk.gdk.Event`.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        treeview.handler_block(self._lst_handler_id[1])

        # The cursor-changed signal will call the _on_change_row.  If
        # _on_change_row is called from here, it gets called twice.  Once on
        # the currently selected row and once on the newly selected row.  Thus,
        # we don't need (or want) to respond to left button clicks.
        if event.button == 3:
            print "FIXME: Rick clicking should launch a pop-up menu with " \
                  "options to insert sibling, insert child, delete " \
                  "(selected), save (selected), and save all in " \
                  "rtk.gui.gtk.workviews.SimilarItem._on_button_press()."

        treeview.handler_unblock(self._lst_handler_id[1])

        return _return

    def _on_combo_changed(self, combo, index):
        """
        Respond to gtk.ComboBox() 'changed' signals.

        :param gtk.ComboBox combo: the gtk.ComboBox() that called this method.
        :param int index: the index in the handler ID list oc the callback
                          signal associated with the gtk.ComboBox() that
                          called this method.
        :return: False if successful or True is an error is encountered.
        :rtype: bool
        """
        _return = False
        _visible = []
        _editable = []

        combo.handler_block(self._lst_handler_id[index])

        _method_id = combo.get_active()
        _parent = self._dtc_data_controller.request_select(self._parent_id)

        if _parent is not None:
            _parent.method_id = _method_id
            for _child in self._dtc_data_controller.request_select_children(
                    self._parent_id):
                _child.data.method_id = _method_id

            if _parent.method_id == 1:  # Topic 633.
                _visible = [2, 3, 4, 5, 6, 7, 8, 9, 35]
                _editable = [
                    4,
                    5,
                    6,
                    7,
                    8,
                    9,
                ]

            elif _parent.method_id == 2:  # User-defined
                _editable = []
                _visible = []
                for _index, _value in enumerate(self.treeview.visible):
                    if _value == 1:
                        _visible.append(_index)
                for _index, _value in enumerate(self.treeview.editable):
                    if _value == 1:
                        _editable.append(_index)

            _return = self._do_set_visible(_visible, _editable)

        combo.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_select(self, module_id):
        """
        Respond to the `selectedHardware` signal from pypubsub.

        :param int module_id: the ID of the Hardware that was selected.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self._parent_id = module_id

        try:
            self._method_id = self._dtc_data_controller.request_select(
                self._parent_id).method_id
        except AttributeError:
            self._method_id = 0

        self.cmbSimilarItemMethod.handler_block(self._lst_handler_id[2])
        self.cmbSimilarItemMethod.set_active(self._method_id)
        self.cmbSimilarItemMethod.handler_unblock(self._lst_handler_id[2])

        _nodes = self._dtc_data_controller.request_select_children(
            self._parent_id)

        return self._do_load_tree(_nodes)

    def _on_select_revision(self, module_id):
        """
        Respond to the `selectedRevision` signal from pypubsub.

        This method is called whenever a new Revision is selected in the RTK
        Module View.  It selects all the Similar Item for the Revision ID
        passedand builds the treelib Tree() to hold them all for use.

        :param int module_id: the Revision ID to select the SimilarItem for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self._revision_id = module_id

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RTKBaseView.__init__
        self._dtc_data_controller = \
            self._mdcRTK.dic_controllers['similaritem']
        _tree = self._dtc_data_controller.request_select_all(module_id)

        self._dtc_hw_controller = self._mdcRTK.dic_controllers['hardware']

        return _return

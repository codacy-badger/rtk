# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.workviews.HazOps.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""HazOps Work View."""

from sortedcontainers import SortedDict
from pubsub import pub

# Import other RTK modules.
from rtk.Configuration import RTK_FAILURE_PROBABILITY
from rtk.gui.gtk import rtk
from rtk.gui.gtk.rtk.Widget import _, gtk, gobject
from .WorkView import RTKWorkView


class HazOps(RTKWorkView):
    """
    Display HazOps attribute data in the Work Book.

    The WorkView displays all the attributes for the Failure Mode and Effects
    Analysis (HazOps). The attributes of a HazOps Work View are:

    :ivar _lst_handler_id: list containing the ID's of the callback signals for
                           each gtk.Widget() associated with an editable
                           Functional HazOps attribute.

    +-------+-------------------------------------------+
    | Index | Widget - Signal                           |
    +=======+===========================================+
    |   0   | tvw_hazops `cursor_changed`               |
    +-------+-------------------------------------------+
    |   1   | tvw_hazops `button_press_event`           |
    +-------+-------------------------------------------+
    |   2   | tvw_hazops `edited`                       |
    +-------+-------------------------------------------+
    """

    def __init__(self, controller):
        """
        Initialize the Work View for the HazOps.

        :param controller: the RTK master data controller instance.
        :type controller: :class:`rtk.RTK.RTK`
        """
        RTKWorkView.__init__(self, controller, module='HazOps')

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._revision_id = None
        self._hardware_id = None
        self._hazops_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        _bg_color = '#FFFFFF'
        _fg_color = '#000000'
        _fmt_file = controller.RTK_CONFIGURATION.RTK_CONF_DIR + \
            '/' + controller.RTK_CONFIGURATION.RTK_FORMAT_FILE['hazops']
        _fmt_path = "/root/tree[@name='HazOps']/column"
        _tooltip = _(u"Displays the HazOps Analysis for the currently "
                     u"selected Hardware item.")

        self.treeview = rtk.RTKTreeView(
            _fmt_path, 0, _fmt_file, _bg_color, _fg_color, pixbuf=False)
        self._lst_col_order = self.treeview.order
        self.treeview.set_tooltip_text(_tooltip)

        # Load the potential hazards into the gtk.CellRendererCombo().
        _model = self._do_get_cell_model(3)
        for _key in controller.RTK_CONFIGURATION.RTK_HAZARDS:
            _hazard = '{0:s}, {1:s}'.format(
                controller.RTK_CONFIGURATION.RTK_HAZARDS[_key][0],
                controller.RTK_CONFIGURATION.RTK_HAZARDS[_key][1])
            _model.append((_hazard, ))

        # Load the severity classes into the gtk.CellRendererCombo().
        for i in [6, 10, 14, 18]:
            _model = self._do_get_cell_model(i)
            for _key in controller.RTK_CONFIGURATION.RTK_SEVERITY:
                _severity = controller.RTK_CONFIGURATION.RTK_SEVERITY[_key][1]
                _model.append((_severity, ))

        # Load the failure probabilities into the gtk.CellRendererCombo().
        for i in [7, 11, 15, 19]:
            _model = self._do_get_cell_model(i)
            for _item in RTK_FAILURE_PROBABILITY:
                _model.append((_item[0], ))

        self._lst_handler_id.append(
            self.treeview.connect('cursor_changed', self._do_change_row))
        self._lst_handler_id.append(
            self.treeview.connect('button_press_event', self._on_button_press))

        for i in self._lst_col_order[3:]:
            _cell = self.treeview.get_column(
                self._lst_col_order[i]).get_cell_renderers()
            try:
                _cell[0].connect('edited', self._do_edit_cell, i,
                                 self.treeview.get_model())
            except TypeError:
                _cell[0].connect('toggled', self._do_edit_cell, 'new text', i,
                                 self.treeview.get_model())

        _label = rtk.RTKLabel(
            _(u"HazOps"),
            height=30,
            width=-1,
            justify=gtk.JUSTIFY_CENTER,
            tooltip=_(u"Displays the HazOps analysis for the selected "
                      u"hardware item."))
        self.hbx_tab_label.pack_start(_label)

        self.pack_start(self._make_buttonbox(), False, True)
        self.pack_end(self._make_treeview(), True, True)
        self.show_all()

        #pub.subscribe(self._do_refresh_view, 'calculatedHazOps')
        pub.subscribe(self._on_select_revision, 'selectedRevision')
        pub.subscribe(self._on_select, 'selectedHardware')

    def _do_change_row(self, treeview):
        """
        Handle events for the HazOps Tree View RTKTreeView().

        This method is called whenever a Tree View row is activated.

        :param treeview: the HazOps RTKTreeView().
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
            self._hazops_id = _model.get_value(_row, 2)
        except TypeError:
            self._hazops_id = None

        treeview.handler_unblock(self._lst_handler_id[0])

        return _return

    def _do_edit_cell(self, __cell, path, new_text, position, model):
        """
        Handle edits of the HazOps Work View RTKTreeview().

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

            _node_id = '{0:d}.{1:d}'.format(self._hardware_id, self._hazops_id)
            _hazops = self._dtc_data_controller.request_select(_node_id)

            if position == self._lst_col_order[3]:
                _hazops.potential_hazard = model[path][self._lst_col_order[3]]
            elif position == self._lst_col_order[4]:
                _hazops.potential_cause = model[path][self._lst_col_order[4]]
            elif position == self._lst_col_order[5]:
                _hazops.assembly_effect = model[path][self._lst_col_order[5]]
            elif position == self._lst_col_order[6]:
                _hazops.assembly_severity = model[path][self._lst_col_order[6]]
            elif position == self._lst_col_order[7]:
                _hazops.assembly_probability = model[path][self._lst_col_order[
                    7]]
            elif position == self._lst_col_order[9]:
                _hazops.assembly_mitigation = model[path][self._lst_col_order[
                    9]]
            elif position == self._lst_col_order[10]:
                _hazops.assembly_severity_f = model[path][self._lst_col_order[
                    10]]
            elif position == self._lst_col_order[11]:
                _hazops.assembly_probability_f = model[path][
                    self._lst_col_order[11]]
            elif position == self._lst_col_order[13]:
                _hazops.system_effect = model[path][self._lst_col_order[13]]
            elif position == self._lst_col_order[14]:
                _hazops.system_severity = model[path][self._lst_col_order[14]]
            elif position == self._lst_col_order[15]:
                _hazops.system_probability = model[path][self._lst_col_order[
                    15]]
            elif position == self._lst_col_order[17]:
                _hazops.system_mitigation = model[path][self._lst_col_order[
                    17]]
            elif position == self._lst_col_order[18]:
                _hazops.system_severity_f = model[path][self._lst_col_order[
                    18]]
            elif position == self._lst_col_order[19]:
                _hazops.system_probability_f = model[path][self._lst_col_order[
                    19]]
            elif position == self._lst_col_order[21]:
                _hazops.remarks = model[path][self._lst_col_order[21]]
        else:
            _return = True

        return _return

    def _do_get_cell_model(self, column):
        """
        Retrieve the gtk.CellRendererCombo() gtk.TreeModel().

        :param int column: the column number to retrieve the cell from.
        :return: _model
        :rtype: :class:`gtk.TreeModel`
        """
        _column = self.treeview.get_column(column)
        _cell = _column.get_cell_renderers()[0]
        _model = _cell.get_property('model')
        _model.clear()

        return _model

    def _do_load_tree(self, nodes):
        """
        Iterate through the tree and load the HazOps RTKTreeView().

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

            _data = [
                _entity.revision_id, _entity.hardware_id, _entity.hazard_id,
                _entity.potential_hazard, _entity.potential_cause,
                _entity.assembly_effect, _entity.assembly_severity,
                _entity.assembly_probability, _entity.assembly_hri,
                _entity.assembly_mitigation, _entity.assembly_severity_f,
                _entity.assembly_probability_f, _entity.assembly_hri_f,
                _entity.system_effect, _entity.system_severity,
                _entity.system_probability, _entity.system_hri,
                _entity.system_mitigation, _entity.system_severity_f,
                _entity.system_probability_f, _entity.system_hri_f,
                _entity.remarks, _entity.function_1, _entity.function_2,
                _entity.function_3, _entity.function_4, _entity.function_5,
                _entity.result_1, _entity.result_2, _entity.result_3,
                _entity.result_4, _entity.result_5, _entity.user_blob_1,
                _entity.user_blob_2, _entity.user_blob_3, _entity.user_float_1,
                _entity.user_float_2, _entity.user_float_3, _entity.user_int_1,
                _entity.user_int_2, _entity.user_int_3
            ]

            try:
                _row = _model.append(None, _data)
            except TypeError:
                print "FIXME: Handle TypeError in " \
                      "gtk.gui.workviews.HazOps.HazOps._do_load_tree."
                _return = True
            except ValueError:
                print "FIXME: Handle ValueError in " \
                      "gtk.gui.workviews.HazOps.HazOps._do_load_tree."
                _return = True
            except AttributeError:
                print "FIXME: Handle AttributeError in " \
                      "gtk.gui.workviews.HazOps.HazOps._do_load_tree."
                _return = True

            i += 1

        return _return

    def _do_request_calculate(self, __button):
        """
        Request to calculate the HazOps HRI.

        :param __button: the gtk.ToolButton() that called this method.
        :return: False if sucessful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _model = self.treeview.get_model()
        _row = _model.get_iter_first()

        # Iterate through the hazards and calculate the HRIs.
        while _row is not None:
            _node_id = '{0:d}.{1:d}'.format(
                _model.get_value(_row, 1), _model.get_value(_row, 2))
            _return = (_return or
                       self._dtc_data_controller.request_calculate(_node_id))
            _row = _model.iter_next(_row)

        if not _return:
            _nodes = self._dtc_data_controller.request_select_children(
                self._hardware_id)
            self._do_load_tree(_nodes)

        return _return

    def _do_request_delete(self, __button):
        """
        Request to delete the selected hazard from the HazOps.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._dtc_data_controller.request_delete(self._hazard_id)

    def _do_request_insert(self, __button):
        """
        Request to insert a new hazard into the HazOps.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._dtc_data_controller.request_insert(
            self._revision_id, hardware_id=self._hardware_id)

    def _do_request_update(self, __button):
        """
        Request to save the selected Hazard.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _node_id = '{0:d}.{1:d}'.format(self._hardware_id, self._hazops_id)

        return self._dtc_data_controller.request_update(_node_id)

    def _do_request_update_all(self, __button):
        """
        Request to save all the entities in the HazOps.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._dtc_data_controller.request_update_all(self._hardware_id)

    def _make_buttonbox(self):
        """
        Make the gtk.ButtonBox() for the HazOps class Work View.

        :return: _buttonbox; the gtk.ButtonBox() for the HazOps Work View.
        :rtype: :class:`gtk.ButtonBox`
        """
        _tooltips = [
            _(u"Calculate the HazOps analysis."),
            _(u"Add a hazard to the HazOps analysis."),
            _(u"Remove the selected hazard and all associated data from the "
              u"HazOps analysis."),
            _(u"Save the selected Hazard to the open RTK Program database."),
            _(u"Save all the Hazards for the selected Hardware item to the "
              u"open RTK Program database.")
        ]
        _callbacks = [
            self._do_request_calculate, self._do_request_insert,
            self._do_request_delete, self._do_request_update,
            self._do_request_update_all
        ]
        _icons = ['calculate', 'add', 'remove', 'save', 'save-all']

        _buttonbox = RTKWorkView._make_buttonbox(self, _icons, _tooltips,
                                                 _callbacks, 'vertical')

        return _buttonbox

    def _make_treeview(self):
        """
        Make the HazOps RTKTreeview().

        :return: a gtk.Frame() containing the instance of gtk.Treeview().
        :rtype: :class:`gtk.Frame`
        """
        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.treeview)

        _frame = rtk.RTKFrame(label=_(u"HazOps Analysis"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        self.treeview.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

        return _frame

    def _on_button_press(self, treeview, event):
        """
        Handle mouse clicks on the HazOps Work View RTKTreeView().

        :param treeview: the HazOps TreeView RTKTreeView().
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
                  "rtk.gui.gtk.workviews.HazOps._on_button_press()."

        treeview.handler_unblock(self._lst_handler_id[1])

        return _return

    def _on_select(self, module_id):
        """
        Respond to the `selectedHardware` signal from pypubsub.

        :param int module_id: the ID of the Hardware that was selected.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self._hardware_id = module_id

        _nodes = self._dtc_data_controller.request_select_children(
            self._hardware_id)

        return self._do_load_tree(_nodes)

    def _on_select_revision(self, module_id):
        """
        Respond to the `selectedRevision` signal from pypubsub.

        This method is called whenever a new Revision is selected in the RTK
        Module View.  It selects all the HazOps for the Revision ID passed
        and builds the treelib Tree() to hold them all for use.

        :param int module_id: the Revision ID to select the HazOps for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self._revision_id = module_id

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RTKBaseView.__init__
        self._dtc_data_controller = \
            self._mdcRTK.dic_controllers['hazops']
        _tree = self._dtc_data_controller.request_select_all(module_id)

        return _return

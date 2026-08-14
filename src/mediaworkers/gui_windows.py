from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout

from gardensunion.base.gui_entities_list import EntitiesList
from gardensunion.base.gui_entity import GUIEntity
from gardensunion.base.gui_entity_windows import EntityWindow

from mediaworkers.models import Sketch


class SketchWindow(EntityWindow):
    links = ()

    def build_form(self):
        layout = QVBoxLayout()
        field_names = ['name']
        for field_name in field_names:
            layout_line = self.build_row(field_name)
            layout.addLayout(layout_line)

        return layout


class GUISketch(GUIEntity):
    dj_model = Sketch
    table_class = EntitiesList
    window_class = SketchWindow
    table_fields = ['name']
    field_order = 'name'
    fields_search = ['name']

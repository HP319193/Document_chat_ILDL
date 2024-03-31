from __future__ import annotations
from gradio.themes.base import Base
from gradio.themes.utils import colors, fonts, sizes
from typing import Iterable

class Seafoam(Base):
    def __init__(
        self,
        *,
        primary_hue: colors.Color | str = colors.stone,
        secondary_hue: colors.Color | str = colors.stone,
        neutral_hue: colors.Color | str = colors.stone,
        spacing_size: sizes.Size | str = sizes.spacing_sm,
        radius_size: sizes.Size | str = sizes.radius_sm,
        text_size: sizes.Size | str = sizes.text_sm,
        font: fonts.Font | str | Iterable[fonts.Font | str] = (
            "sans-serif"    
        ),
        font_mono: fonts.Font | str | Iterable[fonts.Font | str] = (
            "monospace"
        ),
    ):
        super().__init__(
            primary_hue=primary_hue,
            secondary_hue=secondary_hue,
            neutral_hue=neutral_hue,
            spacing_size=spacing_size,
            radius_size=radius_size,
            text_size=text_size,
            font=font,
            font_mono=font_mono,
        )
        self.name = "ram"
        super().set(
            # button_shadow="*shadow_drop",
            # button_shadow_hover="*shadow_drop_lg",
            # button_shadow_active="*shadow_inset",
            stat_background_fill="linear-gradient(to right, *primary_400, *primary_200)",
            stat_background_fill_dark="linear-gradient(to right, *primary_400, *primary_600)",
            button_primary_background_fill="#009fae",
            button_primary_background_fill_hover="#009fae",
            button_primary_background_fill_hover_dark="#009fae",
            button_primary_border_color_dark="*primary_500",
            button_secondary_background_fill="#009fae",
            button_secondary_background_fill_dark="#009fae",
            button_secondary_background_fill_hover="#009fae",
            button_secondary_background_fill_hover_dark="#009fae",
            background_fill_primary="*neutral_50",
            # error_text_color="#FF0000",
            # body_text_color="#36454F",
            # body_text_color_dark="#222121",
            # input_background_fill="white",
            body_text_size=sizes.text_md,
            #button_primary_background_fill_hover="*primary_400",
            #button_primary_background_fill_hover_dark="*primary_500",
            #button_secondary_background_fill="white",
            #button_secondary_background_fill_hover="*neutral_100",
            #button_secondary_background_fill_hover_dark="*primary_500",
            block_shadow="*shadow_drop_sm",
            shadow_spread="1px",
            #button_shadow="*shadow_drop_sm",
            button_small_padding="1px",
            button_large_padding="1px",
            block_border_width="1px",
            panel_border_width="1px",
            block_label_text_size="*text_md",
            input_border_width="1px",
            input_background_fill_dark="*neutral_800",
            button_primary_text_color="black",
        )

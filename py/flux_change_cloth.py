class FluxClothChange:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "base_image": ("IMAGE", ""),
                "fill_model": ("MODEL", {"tooltip": "Flux fill model"}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "fluxClothChange"
    CATEGORY = "image"
    OUTPUT_IS_LIST = (True,)

    def fluxClothChange(self, model):
        results = []
        return (results,)

NODE_CLASS_MAPPINGS = {
    "FluxClothChange|Phuong": FluxClothChange,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FluxClothChange|Phuong": "FluxClothChange🐍",
}
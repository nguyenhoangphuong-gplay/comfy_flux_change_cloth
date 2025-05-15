class FluxClothChange:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "max_width": ("INT", {"default": 1024, "min": 0}),
                "max_height": ("INT", {"default": 1024, "min": 0}),
                "min_width": ("INT", {"default": 0, "min": 0}),
                "min_height": ("INT", {"default": 0, "min": 0}),
                "crop_if_required": (["yes", "no"], {"default": "no"}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "fluxClothChange"
    CATEGORY = "image"
    OUTPUT_IS_LIST = (True,)

    def fluxClothChange(self, images, max_width, max_height, min_width, min_height, crop_if_required):
        crop_if_required = crop_if_required == "yes"
        results = []
        return (results,)

NODE_CLASS_MAPPINGS = {
    "FluxClothChange|Phuong": FluxClothChange,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FluxClothChange|Phuong": "FluxClothChange🐍",
}
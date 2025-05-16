import torch
import folder_paths

import comfy
from comfy.patcher_extension import CallbacksMP

class DiffusionModelLoaderKJ():
    # @classmethod
    # def INPUT_TYPES(s):
    #     return {"required": {
    #         "model_name": (folder_paths.get_filename_list("diffusion_models"),
    #                        {"tooltip": "The name of the checkpoint (model) to load."}),
    #         "weight_dtype": (["default", "fp8_e4m3fn", "fp8_e4m3fn_fast", "fp8_e5m2", "fp16", "bf16", "fp32"],),
    #         "compute_dtype": (["default", "fp16", "bf16", "fp32"],
    #                           {"default": "default", "tooltip": "The compute dtype to use for the model."}),
    #         "patch_cublaslinear": ("BOOLEAN", {"default": False,
    #                                            "tooltip": "Enable or disable the patching, won't take effect on already loaded models!"}),
    #         "sage_attention": (["disabled", "auto", "sageattn_qk_int8_pv_fp16_cuda", "sageattn_qk_int8_pv_fp16_triton",
    #                             "sageattn_qk_int8_pv_fp8_cuda"],
    #                            {"default": False, "tooltip": "Patch comfy attention to use sageattn."}),
    #         "enable_fp16_accumulation": ("BOOLEAN", {"default": False,
    #                                                  "tooltip": "Enable torch.backends.cuda.matmul.allow_fp16_accumulation, requires pytorch 2.7.0 nightly."}),
    #     }}

    def patch_and_load(self, model_name, weight_dtype, compute_dtype, patch_cublaslinear, sage_attention,
                       enable_fp16_accumulation):
        DTYPE_MAP = {
            "fp8_e4m3fn": torch.float8_e4m3fn,
            "fp8_e5m2": torch.float8_e5m2,
            "fp16": torch.float16,
            "bf16": torch.bfloat16,
            "fp32": torch.float32
        }
        model_options = {}
        if dtype := DTYPE_MAP.get(weight_dtype):
            model_options["dtype"] = dtype
            print(f"Setting {model_name} weight dtype to {dtype}")

        if weight_dtype == "fp8_e4m3fn_fast":
            model_options["dtype"] = torch.float8_e4m3fn
            model_options["fp8_optimizations"] = True

        if enable_fp16_accumulation:
            if hasattr(torch.backends.cuda.matmul, "allow_fp16_accumulation"):
                torch.backends.cuda.matmul.allow_fp16_accumulation = True
            else:
                raise RuntimeError("Failed to set fp16 accumulation, this requires pytorch 2.7.0 nightly currently")
        else:
            if hasattr(torch.backends.cuda.matmul, "allow_fp16_accumulation"):
                torch.backends.cuda.matmul.allow_fp16_accumulation = False

        unet_path = folder_paths.get_full_path_or_raise("diffusion_models", model_name)
        model = comfy.sd.load_diffusion_model(unet_path, model_options=model_options)
        if dtype := DTYPE_MAP.get(compute_dtype):
            model.set_model_compute_dtype(dtype)
            model.force_cast_weights = False
            print(f"Setting {model_name} compute dtype to {dtype}")

        # def patch_attention(model):
        #     self._patch_modules(patch_cublaslinear, sage_attention)
        #
        # model.add_callback(CallbacksMP.ON_PRE_RUN, patch_attention)

        return (model,)
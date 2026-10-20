%global pypi_name rapidocr

Name:           python-%{pypi_name}
Version:        3.10.0
Release:        1%{?dist}
Summary:        Awesome OCR Library

License:        Apache-2.0
URL:            https://github.com/RapidAI/RapidOCR
Source:         %{url}/archive/refs/tags/v%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel

# Test dependencies
BuildRequires:  python3dist(pytest)
BuildRequires:  python3-onnxruntime
BuildRequires:  python3-openvino
BuildRequires:  python3-torch

%description
Open source OCR for the security of the digital world.

%package -n     python3-%{pypi_name}
Summary:        %{summary}

%description -n python3-%{pypi_name}
Open source OCR for the security of the digital world.

%prep
%autosetup -p1 -n RapidOCR-%{version}

# Fix dep on opencv
sed -i -e 's/opencv-python-headless/opencv/' python/requirements.txt

%generate_buildrequires
cd python
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
%pyproject_buildrequires

%build
cd python
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
%pyproject_wheel

%install
cd python
%pyproject_install
%pyproject_save_files %{pypi_name}

%check
# The MNN, Paddle and TensorRT inference engines are not available in Fedora,
# and some pytorch transforms import a "pytorchocr" module that is not shipped
%pyproject_check_import -e 'rapidocr.inference_engine.mnn*' -e 'rapidocr.inference_engine.paddle*' -e 'rapidocr.inference_engine.tensorrt*' -e 'rapidocr.inference_engine.pytorch.networks.transforms.tbsrn' -e 'rapidocr.inference_engine.pytorch.networks.transforms.tps' -e 'rapidocr.inference_engine.pytorch.networks.transforms.tsrn'
cd python
# Tests that run OCR need to download models from the internet, also skip
# tests for inference engines that are not available in Fedora
%pytest -v --import-mode=append -p no:cacheprovider \
  --ignore=tests/test_cls.py \
  --ignore=tests/test_det_cls_rec.py \
  --ignore=tests/test_engine.py \
  --ignore=tests/test_rec_language.py \
  --ignore=tests/test_return_word.py \
  --ignore=tests/test_to_other_format.py \
  --ignore=tests/test_vis.py \
  --deselect='tests/test_cli.py::test_cli[' \
  --deselect=tests/test_cli.py::test_cli_download_models \
  --deselect=tests/test_cli.py::test_cli_vis[ \
  --deselect=tests/test_cli.py::test_cli_lang_type \
  --deselect=tests/test_default_config.py::test_default_engine_real_full_pipeline \
  --deselect=tests/test_default_config.py::test_default_engine_real_rec_only \
  --deselect=tests/test_input.py::test_exif_transpose \
  --deselect=tests/test_input.py::test_full_black_img \
  --deselect=tests/test_input.py::test_img_url_input \
  --deselect=tests/test_input.py::test_input_bytes \
  --deselect=tests/test_input.py::test_input_memory_image \
  --deselect=tests/test_input.py::test_input_memory_image_matches_bytes \
  --deselect=tests/test_input.py::test_input_parameters \
  --deselect=tests/test_input.py::test_input_path \
  --deselect=tests/test_input.py::test_input_raw_memory_image \
  --deselect=tests/test_input.py::test_input_str \
  --deselect=tests/test_input.py::test_input_three_ndim_one_channel \
  --deselect=tests/test_input.py::test_input_three_ndim_two_channel \
  --deselect=tests/test_input.py::test_letterbox_like \
  --deselect=tests/test_input.py::test_long_img \
  --deselect=tests/test_input.py::test_mode_one_img \
  --deselect=tests/test_input.py::test_transparent_img \
  --deselect=tests/test_input.py::test_zeros

%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.md
%{_bindir}/rapidocr

%changelog
* Tue Oct 20 2026 Mat Booth <mat.booth@gmail.com> - 3.10.0-1
- Initial RapidOCR package


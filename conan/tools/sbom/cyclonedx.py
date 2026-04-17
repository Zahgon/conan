from conan import conan_version


def cyclonedx_1_4(conanfile, name=None, add_build=False, add_tests=False, **kwargs):
    """
    (Experimental) Generate cyclone 1.4 SBOM with JSON format

    Creates a CycloneDX 1.4 Software Bill of Materials (SBOM) from a given dependency graph.



    Parameters:
        conanfile: The conanfile instance.
        name (str, optional): Custom name for the metadata field.
        add_build (bool, optional, default=False): Include build dependencies.
        add_tests (bool, optional, default=False): Include test dependencies.

    Returns:
        The generated CycloneDX 1.4 document as a string.

    Example usage:
    ```
    cyclonedx_1_4(conanfile, name="custom_name", add_build=True, add_test=True, **kwargs)
    ```

    """
    pass


def cyclonedx_1_6(conanfile, name=None, add_build=False, add_tests=False, **kwargs):
    """
    (Experimental) Generate cyclone 1.6 SBOM with JSON format

    Creates a CycloneDX 1.6 Software Bill of Materials (SBOM) from a given dependency graph.



    Parameters:
        conanfile: The conanfile instance.
        name (str, optional): Custom name for the metadata field.
        add_build (bool, optional, default=False): Include build dependencies.
        add_tests (bool, optional, default=False): Include test dependencies.

    Returns:
        The generated CycloneDX 1.6 document as a string.

    Example usage:
    ```
    cyclonedx_1_6(conanfile, name="custom_name", add_build=True, add_test=True, **kwargs)
    ```

    """
    pass


def _calculate_licenses(component):
    pass


def _calculate_bomref(component):
    pass


def should_add_node(node, add_build, add_tests):
    pass

import inspect
import os
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.common import config
import logging
import json
import ckanext.scheming.plugins as scheming  # needed to get custom schemas from outside scheming extension

SPECIAL_INDEX_FIELDS = os.path.join(os.path.dirname(__file__), 'samples/msl_index_fields.json')

log = logging.getLogger(__name__)


def load_config_path(url):
    module, file_name = url.split(':', 1)

    try:
        # __import__ has an odd signature
        m = __import__(module, fromlist=[''])
    except ImportError:
        return

    p = os.path.join(os.path.dirname(inspect.getfile(m)), file_name)

    if os.path.exists(p):
        with open(p) as config_file:
            return json.load(config_file)


class MslIndexRepeatedFieldsPlugin(plugins.SingletonPlugin):
    """
    json.dump repeating dataset fields in before_index to prevent failures
    on unmodified solr schema. It's better to customize your solr schema
    and before_index processing than to use this plugin.
    """
    plugins.implements(plugins.IPackageController, inherit=True)

    SPECIAL_INDEX_FIELDS_OPTION = 'mslindexfields.field_config'

    def before_index(self, data_dict):
        # read special fields for index (must be available in SOLR schema):
        config_setting = config.get(self.SPECIAL_INDEX_FIELDS_OPTION, "")
        if config_setting != "":
            index_dict = load_config_path(config_setting)

            special_index_fields = index_dict['special_index_fields']
            # special_index_fields = ["msl_material", "msl_rock_measured_property"]
            scheming_datasets_plugin = scheming.SchemingDatasetsPlugin()
            schemas = scheming_datasets_plugin.instance._expanded_schemas # read expanded schema's
            if data_dict['type'] not in schemas: # check whether package data_dict of type in expanded_schemas
                return data_dict # if not pass package and return

            definitions = schemas[data_dict['type']]['dataset_fields']
            for definition in definitions: # package is of expanded type, we walk through the schema dataset_fields
                if definition['field_name'] not in data_dict: # if newly defined field is not in package then skip
                    continue
                if 'repeating_subfields' in definition: # if field is in data_dict and is compound
                    for sub_definition in definition['repeating_subfields']:  # traverse schema definition
                        multi_values = set()  # create empty multi-valued set
                        if sub_definition['field_name'] in special_index_fields:  # d_sub['field_name'] is keyname as string
                            # subkey is in special fields for index (e.g. msl_material)
                            for entry in data_dict[definition['field_name']]:  # traverse package
                                if sub_definition['field_name'] in entry:
                                    multi_values.add(entry[sub_definition['field_name']])  # |- Python in-place operator
                            if len(multi_values):
                                data_dict.update({sub_definition['field_name']: sorted(multi_values)})

                    # TODO: convert full parent dict to flattened string: alternative is to remove key from datadict
                    data_dict[definition['field_name']] = json.dumps(data_dict[definition['field_name']])

        return data_dict


class MslFacetsPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IFacets)

    SCHEMA_OPTION = 'mslfacets.dataset_config'

    def dataset_facets(self, facets_dict, package_type):
        config_setting = config.get(self.SCHEMA_OPTION, "")
        if config_setting != "":
            facets_config = load_config_path(config_setting)

            for key in facets_config:
                if package_type == key:
                    return facets_config[key]

            return facets_config['default']

        return facets_dict

    def group_facets(self, facets_dict, group_type, package_type):
        return facets_dict

    def organization_facets(self, facets_dict, organization_type, package_type):
        return facets_dict


class MslCkanUtilPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic',
            'msl_ckan_util')


class MslSearchPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IPackageController, inherit=True)

    def before_search(self, search_params):
        search_params["defType"] = "edismax"
        search_params["mm"] = "1"

        return search_params

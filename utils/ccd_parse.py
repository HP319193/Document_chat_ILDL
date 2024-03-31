
import xml.etree.ElementTree as ET

class HL7Parser:
    def __init__(self, xml_file):
        self.tree = ET.parse(xml_file)
        self.root = self.tree.getroot()
        self.patient_node = self.root.find('.//{urn:hl7-org:v3}patientRole')
        self.author_node = self.root.find('.//{urn:hl7-org:v3}author')
        self.data_enterer_node = self.root.find(
            './/{urn:hl7-org:v3}dataEnterer')
        self.informant_nodes = self.root.findall(
            './/{urn:hl7-org:v3}informant')
        self.component = self.root.find('.//{urn:hl7-org:v3}component')
        self.details = self.extract_details()
        self.aut_details = self.author_details()
        self.data_enterer_details = self.extract_data_enterer_details()
        self.informant_details = self.extract_informant_details()
        self.component_details = self.getComponentDetails()

    def extract_details(self):
        details = {}

        addr_node = self.patient_node.find('.//{urn:hl7-org:v3}addr')
        if addr_node is not None:
            details['address'] = addr_node.findtext(
                '{urn:hl7-org:v3}streetAddressLine', default='')
            details['city'] = addr_node.findtext(
                '{urn:hl7-org:v3}city', default='')
            details['state'] = addr_node.findtext(
                '{urn:hl7-org:v3}state', default='')
            details['postal_code'] = addr_node.findtext(
                '{urn:hl7-org:v3}postalCode', default='')

        # Extract patient details
        name_node = self.patient_node.find('.//{urn:hl7-org:v3}name')
        if name_node is not None:
            prefix = name_node.findtext('{urn:hl7-org:v3}prefix', default='')
            given = name_node.findtext('{urn:hl7-org:v3}given', default='')
            family = name_node.findtext('{urn:hl7-org:v3}family', default='')
            details['patient_name'] = f"{prefix} {given} {family}".strip()
            details['Patient Name'] = f"{prefix} {given} {family}".strip()

        gender_code = self.patient_node.find(
            './/{urn:hl7-org:v3}administrativeGenderCode')
        details['gender_display_name'] = gender_code.get(
            'displayName', default='') if gender_code is not None else None

        birth_time_element = self.patient_node.find(
            './/{urn:hl7-org:v3}birthTime')
        details['birth_time'] = birth_time_element.get(
            'value', default='') if birth_time_element is not None else None

        marital_status_code = self.patient_node.find(
            './/{urn:hl7-org:v3}maritalStatusCode')
        details['is_married'] = marital_status_code.get(
            'displayName', default='') if marital_status_code is not None else None

        religious_affiliation_code = self.patient_node.find(
            './/{urn:hl7-org:v3}religiousAffiliationCode')
        details['religious_code'] = religious_affiliation_code.get(
            'displayName', default='') if religious_affiliation_code is not None else None

        race_code = self.patient_node.find('.//{urn:hl7-org:v3}raceCode')
        details['race'] = race_code.get(
            'displayName', default='') if race_code is not None else None

        ethnic_group_code = self.patient_node.find(
            './/{urn:hl7-org:v3}ethnicGroupCode')
        details['ethnic_code'] = ethnic_group_code.get(
            'displayName', default='') if ethnic_group_code is not None else None
           
        return details

    def author_details(self):
        details = {}
        if self.author_node is not None:
            time_node = self.author_node.find('.//{urn:hl7-org:v3}time')
            details['time'] = time_node.get(
                'value', default='') if time_node is not None else None

            assigned_author_node = self.author_node.find(
                './/{urn:hl7-org:v3}assignedAuthor')

            id_node = assigned_author_node.find('.//{urn:hl7-org:v3}id')
            details['author_id'] = id_node.get(
                'extension', default='') if id_node is not None else None

            addr_node = assigned_author_node.find('.//{urn:hl7-org:v3}addr')
            if addr_node is not None:
                details['author_address'] = addr_node.findtext(
                    '{urn:hl7-org:v3}streetAddressLine', default='')
                details['author_city'] = addr_node.findtext(
                    '{urn:hl7-org:v3}city', default='')
                details['author_state'] = addr_node.findtext(
                    '{urn:hl7-org:v3}state', default='')
                details['author_postal_code'] = addr_node.findtext(
                    '{urn:hl7-org:v3}postalCode', default='')

            telecom_node = assigned_author_node.find(
                './/{urn:hl7-org:v3}telecom')
            details['author_telecom'] = telecom_node.get(
                'value', default='') if telecom_node is not None else None

            assigned_person_node = assigned_author_node.find(
                './/{urn:hl7-org:v3}assignedPerson')
            if assigned_person_node is not None:
                name_node = assigned_person_node.find(
                    './/{urn:hl7-org:v3}name')
                given_name = name_node.findtext(
                    '{urn:hl7-org:v3}given', default='')
                family_name = name_node.findtext(
                    '{urn:hl7-org:v3}family', default='')
                details['author_name'] = f"{given_name} {family_name}"

        return details

    def extract_data_enterer_details(self):
        details = {}

        if self.data_enterer_node is not None:
            assigned_entity_node = self.data_enterer_node.find(
                './/{urn:hl7-org:v3}assignedEntity')

            id_node = assigned_entity_node.find('.//{urn:hl7-org:v3}id')
            details['data_enterer_id'] = id_node.get(
                'extension', default='') if id_node is not None else None

            addr_node = assigned_entity_node.find('.//{urn:hl7-org:v3}addr')
            if addr_node is not None:
                details['data_enterer_address'] = addr_node.findtext(
                    '{urn:hl7-org:v3}streetAddressLine', default='')
                details['data_enterer_city'] = addr_node.findtext(
                    '{urn:hl7-org:v3}city', default='')
                details['data_enterer_state'] = addr_node.findtext(
                    '{urn:hl7-org:v3}state', default='')
                details['data_enterer_postal_code'] = addr_node.findtext(
                    '{urn:hl7-org:v3}postalCode', default='')

            telecom_node = assigned_entity_node.find(
                './/{urn:hl7-org:v3}telecom')
            details['data_enterer_telecom'] = telecom_node.get(
                'value', default='') if telecom_node is not None else None

            assigned_person_node = assigned_entity_node.find(
                './/{urn:hl7-org:v3}assignedPerson')
            if assigned_person_node is not None:
                name_node = assigned_person_node.find(
                    './/{urn:hl7-org:v3}name')
                given_name = name_node.findtext(
                    '{urn:hl7-org:v3}given', default='')
                family_name = name_node.findtext(
                    '{urn:hl7-org:v3}family', default='')
                details['data_enterer_name'] = f"{given_name} {family_name}"

        return details

    def extract_informant_details(self):
        
        informant_details = []
        for informant_node in self.informant_nodes:
            informant = {}
            assigned_entity_node = informant_node.find('.//{urn:hl7-org:v3}assignedEntity')
            if assigned_entity_node is not None:
                id_node = assigned_entity_node.find('.//{urn:hl7-org:v3}id')
                informant['informant_id'] = id_node.get(
                    'extension', default='') if id_node is not None else None

                addr_node = assigned_entity_node.find('.//{urn:hl7-org:v3}addr')
                if addr_node is not None:
                    informant['informant_address'] = addr_node.findtext(
                        '{urn:hl7-org:v3}streetAddressLine', default='')
                    informant['informant_city'] = addr_node.findtext(
                        '{urn:hl7-org:v3}city', default='')
                    informant['informant_state'] = addr_node.findtext(
                        '{urn:hl7-org:v3}state', default='')
                    informant['informant_postal_code'] = addr_node.findtext(
                        '{urn:hl7-org:v3}postalCode', default='')

                telecom_node = assigned_entity_node.find(
                    './/{urn:hl7-org:v3}telecom')
                informant['informant_telecom'] = telecom_node.get(
                    'value', default='') if telecom_node is not None else None

                assigned_person_node = assigned_entity_node.find(
                    './/{urn:hl7-org:v3}assignedPerson')
                if assigned_person_node is not None:
                    name_node = assigned_person_node.find(
                        './/{urn:hl7-org:v3}name')
                    given_name = name_node.findtext(
                        '{urn:hl7-org:v3}given', default='')
                    family_name = name_node.findtext(
                        '{urn:hl7-org:v3}family', default='')
                    informant['informant_name'] = f"{given_name} {family_name}"

            related_entity_node = informant_node.find(
                './/{urn:hl7-org:v3}relatedEntity')
            if related_entity_node is not None:
                informant['related_entity_class_code'] = related_entity_node.get(
                    'classCode', default='')

                code_node = related_entity_node.find('.//{urn:hl7-org:v3}code')
                informant['related_entity_code'] = code_node.get(
                    'code', default='') if code_node is not None else None
                informant['related_entity_display_name'] = code_node.get(
                    'displayName', default='') if code_node is not None else None
                informant['related_entity_code_system'] = code_node.get(
                    'codeSystem', default='') if code_node is not None else None
                informant['related_entity_code_system_name'] = code_node.get(
                    'codeSystemName', default='') if code_node is not None else None

                related_person_node = related_entity_node.find(
                    './/{urn:hl7-org:v3}relatedPerson')
                if related_person_node is not None:
                    name_node = related_person_node.find(
                        './/{urn:hl7-org:v3}name')
                    given_name = name_node.findtext(
                        '{urn:hl7-org:v3}given', default='')
                    family_name = name_node.findtext(
                        '{urn:hl7-org:v3}family', default='')
                    informant['related_entity_name'] = f"{given_name} {family_name}"

            informant_details.append(informant)

        return informant_details
    def extract_table_data(self):

        table_data = []                       
        return table_data
            
    def getComponentDetails(self):
        table_data =[]
        for component_node in self.component:
            section_node = component_node.find('.//{urn:hl7-org:v3}section')
            if section_node:
                section_title = section_node.findtext('.//{urn:hl7-org:v3}/title')
                print('title', section_title)
                text_node = section_node.find('.//{urn:hl7-org:v3}text')
                if text_node:
                    headers = self.extract_table_data()
                    table_data.append(headers)
        return table_data            
            

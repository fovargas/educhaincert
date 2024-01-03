import jsonschema
from jsonschema import validate

# Define the JSON-LD data to validate
json_ld_data = {
    "@context": [
        "https://www.w3.org/2018/credentials/v1",
        "https://w3id.org/blockcerts/schema/3.0/context.json",
        "https://raw.githubusercontent.com/fovargas/blockcertsutpl/main/config/context.json"
    ],
    "type": [
        "VerifiableCredential",
        "BlockcertsCredential"
    ],
    "issuer": "https://raw.githubusercontent.com/fovargas/blockcertsutpl/main/config/profile.json",
    "issuanceDate": "2023-11-15T02:40:30Z",
    "id": "urn:uuid:d862462f-9f30-4f40-a998-dd8b23295ba6",
    "credentialSubject": {
        "id": "did:key:z6MkroHg218ZtsAmbqgNwA91jLx3jpWEj8WSvrq9JDsmU2wo",
        "type": "Student",
        "memberOf": {
            "type": "Organization",
            "subOrganizationOf": {
                "type": "University",
                "id": "did:key:z6MkroHg218ZtsAmbqgNwA91jLx3jpWEj8WSvrq9JDsmU2wo"
            },
            "id": "did:key:z6MkroHg218ZtsAmbqgNwA91jLx3jpWEj8WSvrq9JDsmU2wo"
        }
    },
    "credential": {
        "type": "Microcredential",
        "course": {
            "type": "Course",
            "hasCourseInstructor": {
                "type": "Instructor",
                "id": "did:key:z6MkroHg218ZtsAmbqgNwA91jLx3jpWEj8WSvrq9JDsmU2wo"
            },
            "isPartOf": {
                "type": "LearningPath",
                "name": "Data Science Program"
            },
            "hasLearningOutcome": {
                "type": "LearningOutcome",
                "hasLevelOfMastery": {
                    "type": "LevelOfMastery",
                    "name": "Intermediate"
                },
                "name": "Proficient in Data Analysis"
            },
            "name": "Introduction to Data Science"
        }
    },
    "nonce": ""
}

# Define a generic JSON-LD schema for validation
# Note: This is a very basic schema for demonstration purposes only.
json_ld_schema = {
    "type": "object",
    "properties": {
        "@context": {"type": "array"},
        "type": {"type": "array"},
        "issuer": {"type": "string"},
        "issuanceDate": {"type": "string", "format": "date-time"},
        "id": {"type": "string"},
        "credentialSubject": {"type": "object"},
        "credential": {"type": "object"},
        "nonce": {"type": "string"}
    },
    "required": ["@context", "type", "issuer", "issuanceDate", "id", "credentialSubject", "credential"]
}

# Validate the JSON-LD data
validation_result = ""
try:
    validate(instance=json_ld_data, schema=json_ld_schema)
    validation_result = "Valid JSON-LD"
except jsonschema.exceptions.ValidationError as e:
    validation_result = f"Invalid JSON-LD: {e.message}"

validation_result
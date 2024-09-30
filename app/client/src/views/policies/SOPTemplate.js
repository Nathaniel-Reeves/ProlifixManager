const SOPTemplate = `{
    "document_id": 1,
    "title": "Quality Assurance",
    "subtitle": "Standard Operating Procedure",
    "description": "This is a fake descripton of this fake sop document.",
    "abv": "QA",
    "timestamp_issued": "2020-01-01",
    "timestamp_modified": "2020-01-01",
    "revision": 1,
    "authors": {},
    "chapters": {
        "01": {
            "title": "QA Responsiilities",
            "subtitle": "Standard Operating Procedure",
            "description": "Here is another fake description of this fake sop document.",
            "timestamp_issued": "2020-01-01",
            "timestamp_modified": "2020-01-01",
            "revision": 1,
            "authors": {},
            "employee_training": {
                "user_id": {
                    "date": "2020-01-01",
                    "status": "completed",
                    "trainer": 0
                }
            },
            "regulations": [],
            "sections": {
                "01": {
                    "title": "Purpose",
                    "subtitle": "",
                    "content": ""
                },
                "02": {
                    "title": "Scope",
                    "subtitle": "Standard Operating Procedure",
                    "content": ""
                },
                "03": {
                    "title": "Responsibilities",
                    "subtitle": "Standard Operating Procedure",
                    "content": ""
                },
                "04": {
                    "title": "Materials & Equipment",
                    "subtitle": "Standard Operating Procedure",
                    "content": ""
                },
                "05": {
                    "title": "Documentation",
                    "subtitle": "Standard Operating Procedure",
                    "content": ""
                }
            }
        },
        "02": {
            "title": "QA Responsiilities and stuff",
            "subtitle": "Standard Operating Procedure",
            "description": "",
            "timestamp_issued": "2020-01-01",
            "timestamp_modified": "2020-01-01",
            "revision": 1,
            "authors": [1,2,3],
            "employee_training": {
                "user_id": {
                    "date": "2020-01-01",
                    "status": "completed",
                    "trainer": 0
                }
            },
            "regulations": [],
            "sections": {
                "01": {
                    "title": "Purpose",
                    "subtitle": "Standard Operating Procedure",
                    "content": ""
                },
                "02": {
                    "title": "Scope",
                    "subtitle": "Standard Operating Procedure",
                    "content": ""
                },
                "03": {
                    "title": "Responsibilities",
                    "subtitle": "Standard Operating Procedure",
                    "content": ""
                },
                "04": {
                    "title": "Materials & Equipment",
                    "subtitle": "Standard Operating Procedure",
                    "content": ""
                },
                "05": {
                    "title": "Documentation",
                    "subtitle": "Standard Operating Procedure",
                    "content": ""
                }
            }
        }
    }
}`

export default SOPTemplate

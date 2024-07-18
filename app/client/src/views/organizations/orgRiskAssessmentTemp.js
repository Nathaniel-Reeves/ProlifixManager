const riskAssessment = {
  risk_level_granted: 'High_Risk',
  risk_assesment_id: null,
  assessment_date: null,
  modified_date: null,
  supplier_questionnaire: {
    satisfactory: false,
    request_date: null,
    documents: []
  },
  supplier_certs: {
    satisfactory: false,
    request_date: null,
    documents: []
  },
  food_safety_plan: {
    satisfactory: false,
    request_date: null,
    documents: []
  },
  provides_cofas: false,
  provides_spec_sheets: false,
  is_retail: false,
  out_of_country: false,
  most_recent_test_failure: {
    failed_test: false,
    component_id: null,
    lot_number: null,
    test_date: null,
    documents: []
  },
  user_edit_history: []
}

export default riskAssessment

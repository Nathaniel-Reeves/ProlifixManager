<template>
  <div>
    <h3 id="SupplierRiskAssessments">Supplier Risk Assessments<b-button v-show="!edit" v-b-tooltip.hover :title="'Edit Risk Assessment.'" v-on:click="toggleEdit()" v-bind:class="['btn', 'p-1', 'ml-2', 'btn-light']" type="button"><b-icon icon="pencil-square" class="d-print-none"></b-icon></b-button></h3>

    <b-card v-if="doc_buffer.supplier_risk_assessments.length > 0">
      <div class="d-flex justify-content-between">
        <div>
          <b-card-title>
            <span>Assessment #{{doc_buffer.supplier_risk_assessments[0].risk_assesment_id}}<b-button v-show="!doc_buffer.supplier_risk_assessments[0].edit" v-b-tooltip.hover :title="'Edit Risk Assessment.'" v-on:click="toggleEditAssessment(doc_buffer.supplier_risk_assessments[0])" v-bind:class="['btn', 'p-1', 'ml-2', 'btn-light']" type="button"><b-icon icon="pencil-square" class="d-print-none"></b-icon></b-button></span>
          </b-card-title>
          <h5 class="card-subtitle text-muted mb-2">Created: {{ doc_buffer.supplier_risk_assessments[0].assessment_date }}<br>Modified: {{ doc_buffer.supplier_risk_assessments[0].modified_date }}</h5>
        </div>
        <b-row align-v="center">
          <b-col>
            <b-avatar variant="success" :text="initials(doc_buffer.supplier_risk_assessments[0].user_edit_history.at(-1).user)" :id="'history_avatar_'+doc_buffer.supplier_risk_assessments[0].risk_assesment_id"></b-avatar>
            <b-tooltip :target="'history_avatar_'+doc_buffer.supplier_risk_assessments[0].risk_assesment_id">
              {{ doc_buffer.supplier_risk_assessments[0].user_edit_history.at(-1).action + 'ed by:' }}<br>
              {{ doc_buffer.supplier_risk_assessments[0].user_edit_history.at(-1).user.first_name + ' ' + doc_buffer.supplier_risk_assessments[0].user_edit_history.at(-1).user.last_name }}<br>
              {{ new Date(doc_buffer.supplier_risk_assessments[0].user_edit_history.at(-1).date).toLocaleDateString() }}
            </b-tooltip>
          </b-col>
          <b-col>
            <h1>
              <b-badge v-show="doc_buffer.supplier_risk_assessments[0].risk_level_granted === 'UNKNOWN'" variant="danger" class="mr-2 border">Unknown Risk</b-badge>
              <b-badge v-show="doc_buffer.supplier_risk_assessments[0].risk_level_granted === 'Low_Risk' || doc_buffer.supplier_risk_assessments[0].risk_level_granted === 'No_Risk'" variant="success" class="mr-2 border">Low Risk</b-badge>
              <b-badge v-show="doc_buffer.supplier_risk_assessments[0].risk_level_granted === 'Medium_Risk'" variant="warning" class="mr-2 border">Medium Risk</b-badge>
              <b-badge v-show="doc_buffer.supplier_risk_assessments[0].risk_level_granted === 'High_Risk'" variant="danger" class="mr-2 border">High Risk</b-badge>
            </h1>
          </b-col>
        </b-row>
      </div>
      <b-card-body>
        <div>
          <b-row class="mb-3">
            <b-col><label for="supplier_questionnaire"><strong>Supplier Questionnaire</strong></label></b-col>
          </b-row>
          <b-row class="mb-3">
            <b-col>
              <b-form-datepicker
                :id="'p-supplier_questionnaire-request_date-'+doc_buffer.supplier_risk_assessments[0].risk_assesment_id"
                v-model="doc_buffer.supplier_risk_assessments[0].supplier_questionnaire.request_date"
                :max="new Date()"
                :readonly="!doc_buffer.supplier_risk_assessments[0].edit"
                :disabled="!doc_buffer.supplier_risk_assessments[0].edit"
              ></b-form-datepicker>
            </b-col>
            <b-col style="max-width:fit-content;">
              <strong>Satisfied: </strong>
            </b-col>
            <b-col>
              <div v-if="!doc_buffer.supplier_risk_assessments[0].edit">
                <span v-show="doc_buffer.supplier_risk_assessments[0].supplier_questionnaire.satisfactory" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</span>
                <span v-show="!doc_buffer.supplier_risk_assessments[0].supplier_questionnaire.satisfactory" class="badge badge-danger badge-pill" style="font-size: 1.5em;">No</span>
              </div>
              <div v-else>
                <b-button :disabled="!doc_buffer.supplier_risk_assessments[0].supplier_questionnaire.request_date && doc_buffer.supplier_risk_assessments[0].supplier_questionnaire.documents.length == 0" @click="doc_buffer.supplier_risk_assessments[0].supplier_questionnaire.satisfactory = false;calRL(doc_buffer.supplier_risk_assessments[0])" v-show="doc_buffer.supplier_risk_assessments[0].supplier_questionnaire.satisfactory" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</b-button>
                <b-button :disabled="!doc_buffer.supplier_risk_assessments[0].supplier_questionnaire.request_date && doc_buffer.supplier_risk_assessments[0].supplier_questionnaire.documents.length == 0" @click="doc_buffer.supplier_risk_assessments[0].supplier_questionnaire.satisfactory = true;calRL(doc_buffer.supplier_risk_assessments[0])" v-show="!doc_buffer.supplier_risk_assessments[0].supplier_questionnaire.satisfactory" class="badge badge-danger badge-pill" style="font-size: 1.5em;">No</b-button>
              </div>
            </b-col>
          </b-row>
          <b-row class="mb-3">
            <b-card-group class="ml-3">
              <div v-for="(document, index) in doc_buffer.supplier_risk_assessments[0].supplier_questionnaire.documents" :key="index">
                <b-card class="m-2" style="min-width: 22rem; max-width: 22rem;" no-body>
                  <b-card-body>
                    <b-card-title class="my-1" v-show="document.document_type">
                      {{ document.document_type === 'questionnaire' ? 'Questionnaire' : null }}
                      {{ document.document_type === 'certificate' ? 'Certificate' : null }}
                      {{ document.document_type === 'food_safety_plan' ? 'Food Safety Plan' : null }}
                      {{ document.document_type === 'flow_chart' ? 'Flow Chart' : null }}
                      {{ document.document_type === 'audit' ? 'Audit' : null }}
                      {{ document.document_type === 'letter' ? 'Letter' : null }}
                      {{ document.document_type === 'other' ? 'Other' : null }}
                    </b-card-title>
                    <v-select v-show="!document.document_type" v-model="document.document_type" required label="text" :reduce="doc => doc.value" placeholder="Select Document Type"
                      :options="[
                        { value: 'questionnaire', text: 'Questionnaire' },
                        // { value: 'certificate', text: 'Certificate' },
                        // { value: 'food_safety_plan', text: 'Food Safety Plan' },
                        // { value: 'flow_chart', text: 'Flow Chart' },
                        { value: 'audit', text: 'Audit' },
                        { value: 'letter', text: 'Letter' },
                        { value: 'other', text: 'Other' }
                      ]">
                    </v-select>
                    <strong>Document Name: </strong><br><b-form-input :disabled="!doc_buffer.supplier_risk_assessments[0].edit" v-model="document.name" type="text" class="my-1"></b-form-input>
                    <strong>Description: </strong><br><b-form-textarea :disabled="!doc_buffer.supplier_risk_assessments[0].edit" v-model="document.description" class="my-1" rows="3" max-rows="3"></b-form-textarea>
                    <b-form-file v-if="!document.file_hash && doc_buffer.supplier_risk_assessments[0].edit" :disabled="!document.document_type || !document.name" no-drop accept="image/png, image/jpeg, application/pdf" type="file" class="my-2" @change="onFileChange($event, document)"></b-form-file>
                    <b-button :disabled="!document.document_type || !document.name || !document.file_pointer" block :href="getFile(document)" target="_blank" class="btn-light">View Document</b-button>
                  </b-card-body>
                  <b-card-footer>
                    <b-button block v-show="doc_buffer.supplier_risk_assessments[0].edit" :disabled="!document.document_type || !document.name" variant="outline-danger" @click="deleteDocument(doc_buffer.supplier_risk_assessments[0].supplier_questionnaire.documents, document)">Delete Document</b-button>
                    <div v-show="!doc_buffer.supplier_risk_assessments[0].edit">Upload Date: {{ new Date(document.date_uploaded).toLocaleDateString() }}</div>
                  </b-card-footer>
                </b-card>
              </div>
              <b-card class="m-2" v-if="doc_buffer.supplier_risk_assessments[0].edit" style="min-width: 22rem; max-width: 22rem; cursor: pointer;" @click="addDocument(doc_buffer.supplier_risk_assessments[0].supplier_questionnaire.documents, num_risk_assessments)">
                <b-card-title>Add Document</b-card-title>
              </b-card>
            </b-card-group>
          </b-row>
          <b-row class="mb-3">
            <b-col><label for="supplier_certs"><strong>Supplier Certifications</strong></label></b-col>
          </b-row>
          <b-row class="mb-3">
            <b-col>
              <b-form-datepicker
                :id="'p-supplier_certs-request_date-'+doc_buffer.supplier_risk_assessments[0].risk_assesment_id"
                v-model="doc_buffer.supplier_risk_assessments[0].supplier_certs.request_date"
                :max="new Date()"
                :readonly="!doc_buffer.supplier_risk_assessments[0].edit"
                :disabled="!doc_buffer.supplier_risk_assessments[0].edit"
              ></b-form-datepicker>
            </b-col>
            <b-col style="max-width:fit-content;">
              <strong>Satisfied: </strong>
            </b-col>
            <b-col>
              <div v-if="!doc_buffer.supplier_risk_assessments[0].edit">
                <span v-show="doc_buffer.supplier_risk_assessments[0].supplier_certs.satisfactory" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</span>
                <span v-show="!doc_buffer.supplier_risk_assessments[0].supplier_certs.satisfactory" class="badge badge-danger badge-pill" style="font-size: 1.5em;">No</span>
              </div>
              <div v-else>
                <b-button :disabled="!doc_buffer.supplier_risk_assessments[0].supplier_certs.request_date && doc_buffer.supplier_risk_assessments[0].supplier_certs.documents.length == 0" @click="doc_buffer.supplier_risk_assessments[0].supplier_certs.satisfactory = false;calRL(doc_buffer.supplier_risk_assessments[0])" v-show="doc_buffer.supplier_risk_assessments[0].supplier_certs.satisfactory" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</b-button>
                <b-button :disabled="!doc_buffer.supplier_risk_assessments[0].supplier_certs.request_date && doc_buffer.supplier_risk_assessments[0].supplier_certs.documents.length == 0" @click="doc_buffer.supplier_risk_assessments[0].supplier_certs.satisfactory = true;calRL(doc_buffer.supplier_risk_assessments[0])" v-show="!doc_buffer.supplier_risk_assessments[0].supplier_certs.satisfactory" class="badge badge-danger badge-pill" style="font-size: 1.5em;">No</b-button>
              </div>
            </b-col>
          </b-row>
          <b-row class="mb-3">
            <b-card-group class="ml-3">
              <div v-for="(document, index) in doc_buffer.supplier_risk_assessments[0].supplier_certs.documents" :key="index">
                <b-card class="m-2" style="min-width: 22rem; max-width: 22rem;" no-body>
                  <b-card-body>
                    <b-card-title class="my-1" v-show="document.document_type">
                      {{ document.document_type === 'questionnaire' ? 'Questionnaire' : null }}
                      {{ document.document_type === 'certificate' ? 'Certificate' : null }}
                      {{ document.document_type === 'food_safety_plan' ? 'Food Safety Plan' : null }}
                      {{ document.document_type === 'flow_chart' ? 'Flow Chart' : null }}
                      {{ document.document_type === 'audit' ? 'Audit' : null }}
                      {{ document.document_type === 'letter' ? 'Letter' : null }}
                      {{ document.document_type === 'other' ? 'Other' : null }}
                    </b-card-title>
                    <v-select v-show="!document.document_type" v-model="document.document_type" required label="text" :reduce="doc => doc.value" placeholder="Select Document Type"
                      :options="[
                        // { value: 'questionnaire', text: 'Questionnaire' },
                        { value: 'certificate', text: 'Certificate' },
                        // { value: 'food_safety_plan', text: 'Food Safety Plan' },
                        // { value: 'flow_chart', text: 'Flow Chart' },
                        // { value: 'audit', text: 'Audit' },
                        { value: 'letter', text: 'Letter' },
                        { value: 'other', text: 'Other' }
                      ]">
                    </v-select>
                    <strong>Document Name: </strong><br><b-form-input :disabled="!doc_buffer.supplier_risk_assessments[0].edit" v-model="document.name" type="text" class="my-1"></b-form-input>
                    <strong>Description: </strong><br><b-form-textarea :disabled="!doc_buffer.supplier_risk_assessments[0].edit" v-model="document.description" class="my-1" rows="3" max-rows="3"></b-form-textarea>
                    <b-form-file v-if="!document.file_hash && doc_buffer.supplier_risk_assessments[0].edit" :disabled="!document.document_type || !document.name" no-drop accept="image/png, image/jpeg, application/pdf" type="file" class="my-2" @change="onFileChange($event, document)"></b-form-file>
                    <b-button :disabled="!document.document_type || !document.name || !document.file_pointer" block :href="getFile(document)" target="_blank" class="btn-light">View Document</b-button>
                  </b-card-body>
                  <b-card-footer>
                    <b-button block v-show="doc_buffer.supplier_risk_assessments[0].edit" :disabled="!document.document_type || !document.name" variant="outline-danger" @click="deleteDocument(doc_buffer.supplier_risk_assessments[0].supplier_questionnaire.documents, document)">Delete Document</b-button>
                    <div v-show="!doc_buffer.supplier_risk_assessments[0].edit">Upload Date: {{ new Date(document.date_uploaded).toLocaleDateString() }}</div>
                  </b-card-footer>
                </b-card>
              </div>
              <b-card class="m-2" v-if="doc_buffer.supplier_risk_assessments[0].edit" style="min-width: 22rem; max-width: 22rem; cursor: pointer;" @click="addDocument(doc_buffer.supplier_risk_assessments[0].supplier_questionnaire.documents, num_risk_assessments)">
                <b-card-title>Add Document</b-card-title>
              </b-card>
            </b-card-group>
          </b-row>
          <b-row class="mb-3">
            <b-col><label for="food_safety_plan"><strong>Food Safety Plan</strong></label></b-col>
          </b-row>
          <b-row class="mb-3">
            <b-col>
              <b-form-datepicker
                :id="'p-food_safety_plan-request_date-'+doc_buffer.supplier_risk_assessments[0].risk_assesment_id"
                v-model="doc_buffer.supplier_risk_assessments[0].food_safety_plan.request_date"
                :max="new Date()"
                :readonly="!doc_buffer.supplier_risk_assessments[0].edit"
                :disabled="!doc_buffer.supplier_risk_assessments[0].edit"
              ></b-form-datepicker>
            </b-col>
            <b-col style="max-width:fit-content;">
              <strong>Satisfied: </strong>
            </b-col>
            <b-col>
              <div v-if="!doc_buffer.supplier_risk_assessments[0].edit">
                <span v-show="doc_buffer.supplier_risk_assessments[0].food_safety_plan.satisfactory" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</span>
                <span v-show="!doc_buffer.supplier_risk_assessments[0].food_safety_plan.satisfactory" class="badge badge-danger badge-pill" style="font-size: 1.5em;">No</span>
              </div>
              <div v-else>
                <b-button :disabled="!doc_buffer.supplier_risk_assessments[0].food_safety_plan.request_date && doc_buffer.supplier_risk_assessments[0].food_safety_plan.documents.length == 0" @click="doc_buffer.supplier_risk_assessments[0].food_safety_plan.satisfactory = false;calRL(doc_buffer.supplier_risk_assessments[0])" v-show="doc_buffer.supplier_risk_assessments[0].food_safety_plan.satisfactory" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</b-button>
                <b-button :disabled="!doc_buffer.supplier_risk_assessments[0].food_safety_plan.request_date && doc_buffer.supplier_risk_assessments[0].food_safety_plan.documents.length == 0" @click="doc_buffer.supplier_risk_assessments[0].food_safety_plan.satisfactory = true;calRL(doc_buffer.supplier_risk_assessments[0])" v-show="!doc_buffer.supplier_risk_assessments[0].food_safety_plan.satisfactory" class="badge badge-danger badge-pill" style="font-size: 1.5em;">No</b-button>
              </div>
            </b-col>
          </b-row>
          <b-row class="mb-3">
            <b-card-group class="ml-3">
              <div v-for="(document, index) in doc_buffer.supplier_risk_assessments[0].food_safety_plan.documents" :key="index">
                <b-card class="m-2" style="min-width: 22rem; max-width: 22rem;" no-body>
                  <b-card-body>
                    <b-card-title class="my-1" v-show="document.document_type">
                      {{ document.document_type === 'questionnaire' ? 'Questionnaire' : null }}
                      {{ document.document_type === 'certificate' ? 'Certificate' : null }}
                      {{ document.document_type === 'food_safety_plan' ? 'Food Safety Plan' : null }}
                      {{ document.document_type === 'flow_chart' ? 'Flow Chart' : null }}
                      {{ document.document_type === 'audit' ? 'Audit' : null }}
                      {{ document.document_type === 'letter' ? 'Letter' : null }}
                      {{ document.document_type === 'other' ? 'Other' : null }}
                    </b-card-title>
                    <v-select v-show="!document.document_type" v-model="document.document_type" required label="text" :reduce="doc => doc.value" placeholder="Select Document Type"
                      :options="[
                        // { value: 'questionnaire', text: 'Questionnaire' },
                        // { value: 'certificate', text: 'Certificate' },
                        { value: 'food_safety_plan', text: 'Food Safety Plan' },
                        { value: 'flow_chart', text: 'Flow Chart' },
                        { value: 'audit', text: 'Audit' },
                        { value: 'letter', text: 'Letter' },
                        { value: 'other', text: 'Other' }
                      ]">
                    </v-select>
                    <strong>Document Name: </strong><br><b-form-input :disabled="!doc_buffer.supplier_risk_assessments[0].edit" v-model="document.name" type="text" class="my-1"></b-form-input>
                    <strong>Description: </strong><br><b-form-textarea :disabled="!doc_buffer.supplier_risk_assessments[0].edit" v-model="document.description" class="my-1" rows="3" max-rows="3"></b-form-textarea>
                    <b-form-file v-if="!document.file_hash && doc_buffer.supplier_risk_assessments[0].edit" :disabled="!document.document_type || !document.name" no-drop accept="image/png, image/jpeg, application/pdf" type="file" class="my-2" @change="onFileChange($event, document)"></b-form-file>
                    <b-button :disabled="!document.document_type || !document.name || !document.file_pointer" block :href="getFile(document)" target="_blank" class="btn-light">View Document</b-button>
                  </b-card-body>
                  <b-card-footer>
                    <b-button block v-show="doc_buffer.supplier_risk_assessments[0].edit" :disabled="!document.document_type || !document.name" variant="outline-danger" @click="deleteDocument(doc_buffer.supplier_risk_assessments[0].supplier_questionnaire.documents, document)">Delete Document</b-button>
                    <div v-show="!doc_buffer.supplier_risk_assessments[0].edit">Upload Date: {{ new Date(document.date_uploaded).toLocaleDateString() }}</div>
                  </b-card-footer>
                </b-card>
              </div>
              <b-card class="m-2" v-if="doc_buffer.supplier_risk_assessments[0].edit" style="min-width: 22rem; max-width: 22rem; cursor: pointer;" @click="addDocument(doc_buffer.supplier_risk_assessments[0].supplier_questionnaire.documents, num_risk_assessments)">
                <b-card-title>Add Document</b-card-title>
              </b-card>
            </b-card-group>
          </b-row>
          <hr>
          <b-row class="mb-3">
            <b-col style="max-width:fit-content;"><label for="provides_cofas"><strong>Provides CofA's</strong></label></b-col>
            <b-col>
              <div v-if="!doc_buffer.supplier_risk_assessments[0].edit">
                <span v-show="doc_buffer.supplier_risk_assessments[0].provides_cofas" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</span>
                <span v-show="!doc_buffer.supplier_risk_assessments[0].provides_cofas" class="badge badge-danger badge-pill" style="font-size: 1.5em;">No</span>
              </div>
              <div v-else>
                <b-button @click="doc_buffer.supplier_risk_assessments[0].provides_cofas = false;calRL(doc_buffer.supplier_risk_assessments[0])" v-show="doc_buffer.supplier_risk_assessments[0].provides_cofas" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</b-button>
                <b-button @click="doc_buffer.supplier_risk_assessments[0].provides_cofas = true;calRL(doc_buffer.supplier_risk_assessments[0])" v-show="!doc_buffer.supplier_risk_assessments[0].provides_cofas" class="badge badge-danger badge-pill" style="font-size: 1.5em;">No</b-button>
              </div>
            </b-col>
            <b-col style="max-width:fit-content;"><label for="provides_spec_sheets"><strong>Provides Spec Sheets</strong></label></b-col>
            <b-col>
              <div v-if="!doc_buffer.supplier_risk_assessments[0].edit">
                <span v-show="doc_buffer.supplier_risk_assessments[0].provides_spec_sheets" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</span>
                <span v-show="!doc_buffer.supplier_risk_assessments[0].provides_spec_sheets" class="badge badge-danger badge-pill" style="font-size: 1.5em;">No</span>
              </div>
              <div v-else>
                <b-button @click="doc_buffer.supplier_risk_assessments[0].provides_spec_sheets = false;calRL(doc_buffer.supplier_risk_assessments[0])" v-show="doc_buffer.supplier_risk_assessments[0].provides_spec_sheets" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</b-button>
                <b-button @click="doc_buffer.supplier_risk_assessments[0].provides_spec_sheets = true;calRL(doc_buffer.supplier_risk_assessments[0])" v-show="!doc_buffer.supplier_risk_assessments[0].provides_spec_sheets" class="badge badge-danger badge-pill" style="font-size: 1.5em;">No</b-button>
              </div>
            </b-col>
            <b-col style="max-width:fit-content;"><label for="is_retail"><strong>Retail</strong></label></b-col>
            <b-col>
              <div v-if="!doc_buffer.supplier_risk_assessments[0].edit">
                <span v-show="doc_buffer.supplier_risk_assessments[0].is_retail" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</span>
                <span v-show="!doc_buffer.supplier_risk_assessments[0].is_retail" class="badge badge-danger badge-pill" style="font-size: 1.5em;">No</span>
              </div>
              <div v-else>
                <b-button @click="doc_buffer.supplier_risk_assessments[0].is_retail = false;calRL(doc_buffer.supplier_risk_assessments[0])" v-show="doc_buffer.supplier_risk_assessments[0].is_retail" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</b-button>
                <b-button @click="doc_buffer.supplier_risk_assessments[0].is_retail = true;calRL(doc_buffer.supplier_risk_assessments[0])" v-show="!doc_buffer.supplier_risk_assessments[0].is_retail" class="badge badge-danger badge-pill" style="font-size: 1.5em;">No</b-button>
              </div>
            </b-col>
            <b-col style="max-width:fit-content;"><label for="out_of_country"><strong>Out of Country</strong></label></b-col>
            <b-col>
              <div v-if="!doc_buffer.supplier_risk_assessments[0].edit">
                <span v-show="doc_buffer.supplier_risk_assessments[0].out_of_countr" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</span>
                <span v-show="!doc_buffer.supplier_risk_assessments[0].out_of_countr" class="badge badge-danger badge-pill" style="font-size: 1.5em;">No</span>
              </div>
              <div v-else>
                <b-button @click="doc_buffer.supplier_risk_assessments[0].out_of_countr = false;calRL(doc_buffer.supplier_risk_assessments[0])" v-show="doc_buffer.supplier_risk_assessments[0].out_of_countr" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</b-button>
                <b-button @click="doc_buffer.supplier_risk_assessments[0].out_of_countr = true;calRL(doc_buffer.supplier_risk_assessments[0])" v-show="!doc_buffer.supplier_risk_assessments[0].out_of_countr" class="badge badge-danger badge-pill" style="font-size: 1.5em;">No</b-button>
              </div>
            </b-col>
          </b-row>
          <hr>
          <b-row class="mb-3">
            <b-col><label for="most_recent_test_failure"><strong>Most Recent Test Failure</strong></label></b-col>
          </b-row>
        </div>
        <b-button type="submit" v-show="doc_buffer.supplier_risk_assessments[0].edit" variant="outline-success" class="m-2" v-on:click="toggleEditAssessment(doc_buffer.supplier_risk_assessments[0])">Save</b-button>
      </b-card-body>
    </b-card>

    <b-card v-else>
      <b-card-title>
        No Assessments
      </b-card-title>
    </b-card>

    <div class="d-flex justify-content-center m-3" v-if="doc_buffer.supplier_risk_assessments.length > 1">
      <b-button v-show="!show_assessments" @click="show_assessments = true" class="m-1" variant="light">View All Assessments</b-button>
      <b-button v-show="show_assessments" @click="show_assessments = false" class="m-1" variant="light">Hide Assessments</b-button>
    </div>
    <b-collapse v-if="doc_buffer.supplier_risk_assessments.length > 1" id="show_assessments" v-model="show_assessments" style="position:relative; height:800px; overflow-y:scroll;">
      <div v-for="assessment in doc_buffer.supplier_risk_assessments.slice(1)" :key="assessment.risk_assesment_id">
        <b-card>
          <div class="d-flex justify-content-between">
            <div>
              <b-card-title>
                <span>Assessment #{{assessment.risk_assesment_id}}<b-button v-show="!assessment.edit" v-b-tooltip.hover :title="'Edit Risk Assessment.'" v-on:click="toggleEditAssessment(assessment)" v-bind:class="['btn', 'p-1', 'ml-2', 'btn-light']" type="button"><b-icon icon="pencil-square" class="d-print-none"></b-icon></b-button></span>
              </b-card-title>
              <h5 class="card-subtitle text-muted mb-2">Created: {{ assessment.assessment_date }}<br>Modified: {{ assessment.modified_date }}</h5>
            </div>
            <b-row align-v="center">
              <b-col>
                <b-avatar variant="success" :text="initials(assessment.user_edit_history.at(-1).user)" :id="'history_avatar_'+assessment.risk_assesment_id"></b-avatar>
                <b-tooltip :target="'history_avatar_'+assessment.risk_assesment_id">
                  {{ assessment.user_edit_history.at(-1).action + 'ed by:' }}<br>
                  {{ assessment.user_edit_history.at(-1).user.first_name + ' ' + assessment.user_edit_history.at(-1).user.last_name }}<br>
                  {{ new Date(assessment.user_edit_history.at(-1).date).toLocaleDateString() }}
                </b-tooltip>
              </b-col>
              <b-col>
                <h1>
                  <b-badge v-show="assessment.risk_level_granted === 'UNKNOWN'" variant="danger" class="mr-2 border">Unknown Risk</b-badge>
                  <b-badge v-show="assessment.risk_level_granted === 'Low_Risk' || assessment.risk_level_granted === 'No_Risk'" variant="success" class="mr-2 border">Low Risk</b-badge>
                  <b-badge v-show="assessment.risk_level_granted === 'Medium_Risk'" variant="warning" class="mr-2 border">Medium Risk</b-badge>
                  <b-badge v-show="assessment.risk_level_granted === 'High_Risk'" variant="danger" class="mr-2 border">High Risk</b-badge>
                </h1>
              </b-col>
            </b-row>
          </div>
          <b-card-body>
            <div>
              <b-row class="mb-3">
                <b-col><label for="supplier_questionnaire"><strong>Supplier Questionnaire</strong></label></b-col>
              </b-row>
              <b-row class="mb-3">
                <b-col>
                  <b-form-datepicker
                    :id="'supplier_questionnaire-request_date-'+assessment.risk_assesment_id"
                    v-model="assessment.supplier_questionnaire.request_date"
                    :max="new Date()"
                    :readonly="!assessment.edit"
                    :disabled="!assessment.edit"
                  ></b-form-datepicker>
                </b-col>
                <b-col style="max-width:fit-content;">
                  <strong>Satisfied: </strong>
                </b-col>
                <b-col>
                  <div v-if="!assessment.edit">
                    <span v-show="assessment.supplier_questionnaire.satisfactory" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</span>
                    <span v-show="!assessment.supplier_questionnaire.satisfactory" class="badge badge-danger badge-pill" style="font-size: 1.5em;">No</span>
                  </div>
                  <div v-else>
                    <b-button :disabled="!assessment.supplier_questionnaire.request_date && assessment.supplier_questionnaire.documents.length == 0" @click="assessment.supplier_questionnaire.satisfactory = false;calRL(assessment)" v-show="assessment.supplier_questionnaire.satisfactory" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</b-button>
                    <b-button :disabled="!assessment.supplier_questionnaire.request_date && assessment.supplier_questionnaire.documents.length == 0" @click="assessment.supplier_questionnaire.satisfactory = true;calRL(assessment)" v-show="!assessment.supplier_questionnaire.satisfactory" class="badge badge-danger badge-pill" style="font-size: 1.5em;">No</b-button>
                  </div>
                </b-col>
              </b-row>
              <b-row class="mb-3">
                <b-card-group class="ml-3">
                  <div v-for="(document, index) in assessment.supplier_questionnaire.documents" :key="index">
                    <b-card class="m-2" style="min-width: 22rem; max-width: 22rem;" no-body>
                      <b-card-body>
                        <b-card-title class="my-1" v-show="document.document_type">
                          {{ document.document_type === 'questionnaire' ? 'Questionnaire' : null }}
                          {{ document.document_type === 'certificate' ? 'Certificate' : null }}
                          {{ document.document_type === 'food_safety_plan' ? 'Food Safety Plan' : null }}
                          {{ document.document_type === 'flow_chart' ? 'Flow Chart' : null }}
                          {{ document.document_type === 'audit' ? 'Audit' : null }}
                          {{ document.document_type === 'letter' ? 'Letter' : null }}
                          {{ document.document_type === 'other' ? 'Other' : null }}
                        </b-card-title>
                        <v-select v-show="!document.document_type" v-model="document.document_type" required label="text" :reduce="doc => doc.value" placeholder="Select Document Type"
                          :options="[
                            { value: 'questionnaire', text: 'Questionnaire' },
                            // { value: 'certificate', text: 'Certificate' },
                            // { value: 'food_safety_plan', text: 'Food Safety Plan' },
                            // { value: 'flow_chart', text: 'Flow Chart' },
                            { value: 'audit', text: 'Audit' },
                            { value: 'letter', text: 'Letter' },
                            { value: 'other', text: 'Other' }
                          ]">
                        </v-select>
                        <strong>Document Name: </strong><br><b-form-input :disabled="!assessment.edit" v-model="document.name" type="text" class="my-1"></b-form-input>
                        <strong>Description: </strong><br><b-form-textarea :disabled="!assessment.edit" v-model="document.description" class="my-1" rows="3" max-rows="3"></b-form-textarea>
                        <b-form-file v-if="!document.file_hash && assessment.edit" :disabled="!document.document_type || !document.name" no-drop accept="image/png, image/jpeg, application/pdf" type="file" class="my-2" @change="onFileChange($event, document)"></b-form-file>
                        <b-button :disabled="!document.document_type || !document.name || !document.file_pointer" block :href="getFile(document)" target="_blank" class="btn-light">View Document</b-button>
                      </b-card-body>
                      <b-card-footer>
                        <b-button block v-show="assessment.edit" :disabled="!document.document_type || !document.name" variant="outline-danger" @click="deleteDocument(assessment.supplier_questionnaire.documents, document)">Delete Document</b-button>
                        <div v-show="!assessment.edit">Upload Date: {{ new Date(document.date_uploaded).toLocaleDateString() }}</div>
                      </b-card-footer>
                    </b-card>
                  </div>
                  <b-card class="m-2" v-if="assessment.edit" style="min-width: 22rem; max-width: 22rem; cursor: pointer;" @click="addDocument(assessment.supplier_questionnaire.documents, num_risk_assessments)">
                    <b-card-title>Add Document</b-card-title>
                  </b-card>
                </b-card-group>
              </b-row>
              <b-row class="mb-3">
                <b-col><label for="supplier_certs"><strong>Supplier Certifications</strong></label></b-col>
              </b-row>
              <b-row class="mb-3">
                <b-col>
                  <b-form-datepicker
                    :id="'supplier_certs-request_date-'+assessment.risk_assesment_id"
                    v-model="assessment.supplier_certs.request_date"
                    :max="new Date()"
                    :readonly="!assessment.edit"
                    :disabled="!assessment.edit"
                  ></b-form-datepicker>
                </b-col>
                <b-col style="max-width:fit-content;">
                  <strong>Satisfied: </strong>
                </b-col>
                <b-col>
                  <div v-if="!assessment.edit">
                    <span v-show="assessment.supplier_certs.satisfactory" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</span>
                    <span v-show="!assessment.supplier_certs.satisfactory" class="badge badge-danger badge-pill" style="font-size: 1.5em;">No</span>
                  </div>
                  <div v-else>
                    <b-button :disabled="!assessment.supplier_certs.request_date && assessment.supplier_certs.documents.length == 0" @click="assessment.supplier_certs.satisfactory = false;calRL(assessment)" v-show="assessment.supplier_certs.satisfactory" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</b-button>
                    <b-button :disabled="!assessment.supplier_certs.request_date && assessment.supplier_certs.documents.length == 0" @click="assessment.supplier_certs.satisfactory = true;calRL(assessment)" v-show="!assessment.supplier_certs.satisfactory" class="badge badge-danger badge-pill" style="font-size: 1.5em;">No</b-button>
                  </div>
                </b-col>
              </b-row>
              <b-row class="mb-3">
                <b-card-group class="ml-3">
                  <div v-for="(document, index) in assessment.supplier_certs.documents" :key="index">
                    <b-card class="m-2" style="min-width: 22rem; max-width: 22rem;" no-body>
                      <b-card-body>
                        <b-card-title class="my-1" v-show="document.document_type">
                          {{ document.document_type === 'questionnaire' ? 'Questionnaire' : null }}
                          {{ document.document_type === 'certificate' ? 'Certificate' : null }}
                          {{ document.document_type === 'food_safety_plan' ? 'Food Safety Plan' : null }}
                          {{ document.document_type === 'flow_chart' ? 'Flow Chart' : null }}
                          {{ document.document_type === 'audit' ? 'Audit' : null }}
                          {{ document.document_type === 'letter' ? 'Letter' : null }}
                          {{ document.document_type === 'other' ? 'Other' : null }}
                        </b-card-title>
                        <v-select v-show="!document.document_type" v-model="document.document_type" required label="text" :reduce="doc => doc.value" placeholder="Select Document Type"
                          :options="[
                            // { value: 'questionnaire', text: 'Questionnaire' },
                            { value: 'certificate', text: 'Certificate' },
                            // { value: 'food_safety_plan', text: 'Food Safety Plan' },
                            // { value: 'flow_chart', text: 'Flow Chart' },
                            // { value: 'audit', text: 'Audit' },
                            { value: 'letter', text: 'Letter' },
                            { value: 'other', text: 'Other' }
                          ]">
                        </v-select>
                        <strong>Document Name: </strong><br><b-form-input :disabled="!assessment.edit" v-model="document.name" type="text" class="my-1"></b-form-input>
                        <strong>Description: </strong><br><b-form-textarea :disabled="!assessment.edit" v-model="document.description" class="my-1" rows="3" max-rows="3"></b-form-textarea>
                        <b-form-file v-if="!document.file_hash && assessment.edit" :disabled="!document.document_type || !document.name" no-drop accept="image/png, image/jpeg, application/pdf" type="file" class="my-2" @change="onFileChange($event, document)"></b-form-file>
                        <b-button :disabled="!document.document_type || !document.name || !document.file_pointer" block :href="getFile(document)" target="_blank" class="btn-light">View Document</b-button>
                      </b-card-body>
                      <b-card-footer>
                        <b-button block v-show="assessment.edit" :disabled="!document.document_type || !document.name" variant="outline-danger" @click="deleteDocument(assessment.supplier_questionnaire.documents, document)">Delete Document</b-button>
                        <div v-show="!assessment.edit">Upload Date: {{ new Date(document.date_uploaded).toLocaleDateString() }}</div>
                      </b-card-footer>
                    </b-card>
                  </div>
                  <b-card class="m-2" v-if="assessment.edit" style="min-width: 22rem; max-width: 22rem; cursor: pointer;" @click="addDocument(assessment.supplier_questionnaire.documents, num_risk_assessments)">
                    <b-card-title>Add Document</b-card-title>
                  </b-card>
                </b-card-group>
              </b-row>
              <b-row class="mb-3">
                <b-col><label for="food_safety_plan"><strong>Food Safety Plan</strong></label></b-col>
              </b-row>
              <b-row class="mb-3">
                <b-col>
                  <b-form-datepicker
                    :id="'food_safety_plan-request_date-'+assessment.risk_assesment_id"
                    v-model="assessment.food_safety_plan.request_date"
                    :max="new Date()"
                    :readonly="!assessment.edit"
                    :disabled="!assessment.edit"
                  ></b-form-datepicker>
                </b-col>
                <b-col style="max-width:fit-content;">
                  <strong>Satisfied: </strong>
                </b-col>
                <b-col>
                  <div v-if="!assessment.edit">
                    <span v-show="assessment.food_safety_plan.satisfactory" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</span>
                    <span v-show="!assessment.food_safety_plan.satisfactory" class="badge badge-danger badge-pill" style="font-size: 1.5em;">No</span>
                  </div>
                  <div v-else>
                    <b-button :disabled="!assessment.food_safety_plan.request_date && assessment.food_safety_plan.documents.length == 0" @click="assessment.food_safety_plan.satisfactory = false;calRL(assessment)" v-show="assessment.food_safety_plan.satisfactory" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</b-button>
                    <b-button :disabled="!assessment.food_safety_plan.request_date && assessment.food_safety_plan.documents.length == 0" @click="assessment.food_safety_plan.satisfactory = true;calRL(assessment)" v-show="!assessment.food_safety_plan.satisfactory" class="badge badge-danger badge-pill" style="font-size: 1.5em;">No</b-button>
                  </div>
                </b-col>
              </b-row>
              <b-row class="mb-3">
                <b-card-group class="ml-3">
                  <div v-for="(document, index) in assessment.food_safety_plan.documents" :key="index">
                    <b-card class="m-2" style="min-width: 22rem; max-width: 22rem;" no-body>
                      <b-card-body>
                        <b-card-title class="my-1" v-show="document.document_type">
                          {{ document.document_type === 'questionnaire' ? 'Questionnaire' : null }}
                          {{ document.document_type === 'certificate' ? 'Certificate' : null }}
                          {{ document.document_type === 'food_safety_plan' ? 'Food Safety Plan' : null }}
                          {{ document.document_type === 'flow_chart' ? 'Flow Chart' : null }}
                          {{ document.document_type === 'audit' ? 'Audit' : null }}
                          {{ document.document_type === 'letter' ? 'Letter' : null }}
                          {{ document.document_type === 'other' ? 'Other' : null }}
                        </b-card-title>
                        <v-select v-show="!document.document_type" v-model="document.document_type" required label="text" :reduce="doc => doc.value" placeholder="Select Document Type"
                          :options="[
                            // { value: 'questionnaire', text: 'Questionnaire' },
                            // { value: 'certificate', text: 'Certificate' },
                            { value: 'food_safety_plan', text: 'Food Safety Plan' },
                            { value: 'flow_chart', text: 'Flow Chart' },
                            { value: 'audit', text: 'Audit' },
                            { value: 'letter', text: 'Letter' },
                            { value: 'other', text: 'Other' }
                          ]">
                        </v-select>
                        <strong>Document Name: </strong><br><b-form-input :disabled="!assessment.edit" v-model="document.name" type="text" class="my-1"></b-form-input>
                        <strong>Description: </strong><br><b-form-textarea :disabled="!assessment.edit" v-model="document.description" class="my-1" rows="3" max-rows="3"></b-form-textarea>
                        <b-form-file v-if="!document.file_hash && assessment.edit" :disabled="!document.document_type || !document.name" no-drop accept="image/png, image/jpeg, application/pdf" type="file" class="my-2" @change="onFileChange($event, document)"></b-form-file>
                        <b-button :disabled="!document.document_type || !document.name || !document.file_pointer" block :href="getFile(document)" target="_blank" class="btn-light">View Document</b-button>
                      </b-card-body>
                      <b-card-footer>
                        <b-button block v-show="assessment.edit" :disabled="!document.document_type || !document.name" variant="outline-danger" @click="deleteDocument(assessment.supplier_questionnaire.documents, document)">Delete Document</b-button>
                        <div v-show="!assessment.edit">Upload Date: {{ new Date(document.date_uploaded).toLocaleDateString() }}</div>
                      </b-card-footer>
                    </b-card>
                  </div>
                  <b-card class="m-2" v-if="assessment.edit" style="min-width: 22rem; max-width: 22rem; cursor: pointer;" @click="addDocument(assessment.supplier_questionnaire.documents, num_risk_assessments)">
                    <b-card-title>Add Document</b-card-title>
                  </b-card>
                </b-card-group>
              </b-row>
              <hr>
              <b-row class="mb-3">
                <b-col style="max-width:fit-content;"><label for="provides_cofas"><strong>Provides CofA's</strong></label></b-col>
                <b-col>
                  <div v-if="!assessment.edit">
                    <span v-show="assessment.provides_cofas" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</span>
                    <span v-show="!assessment.provides_cofas" class="badge badge-danger badge-pill" style="font-size: 1.5em;">No</span>
                  </div>
                  <div v-else>
                    <b-button @click="assessment.provides_cofas = false;calRL(assessment)" v-show="assessment.provides_cofas" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</b-button>
                    <b-button @click="assessment.provides_cofas = true;calRL(assessment)" v-show="!assessment.provides_cofas" class="badge badge-danger badge-pill" style="font-size: 1.5em;">No</b-button>
                  </div>
                </b-col>
                <b-col style="max-width:fit-content;"><label for="provides_spec_sheets"><strong>Provides Spec Sheets</strong></label></b-col>
                <b-col>
                  <div v-if="!assessment.edit">
                    <span v-show="assessment.provides_spec_sheets" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</span>
                    <span v-show="!assessment.provides_spec_sheets" class="badge badge-danger badge-pill" style="font-size: 1.5em;">No</span>
                  </div>
                  <div v-else>
                    <b-button @click="assessment.provides_spec_sheets = false;calRL(assessment)" v-show="assessment.provides_spec_sheets" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</b-button>
                    <b-button @click="assessment.provides_spec_sheets = true;calRL(assessment)" v-show="!assessment.provides_spec_sheets" class="badge badge-danger badge-pill" style="font-size: 1.5em;">No</b-button>
                  </div>
                </b-col>
                <b-col style="max-width:fit-content;"><label for="is_retail"><strong>Retail</strong></label></b-col>
                <b-col>
                  <div v-if="!assessment.edit">
                    <span v-show="assessment.is_retail" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</span>
                    <span v-show="!assessment.is_retail" class="badge badge-danger badge-pill" style="font-size: 1.5em;">No</span>
                  </div>
                  <div v-else>
                    <b-button @click="assessment.is_retail = false;calRL(assessment)" v-show="assessment.is_retail" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</b-button>
                    <b-button @click="assessment.is_retail = true;calRL(assessment)" v-show="!assessment.is_retail" class="badge badge-danger badge-pill" style="font-size: 1.5em;">No</b-button>
                  </div>
                </b-col>
                <b-col style="max-width:fit-content;"><label for="out_of_country"><strong>Out of Country</strong></label></b-col>
                <b-col>
                  <div v-if="!assessment.edit">
                    <span v-show="assessment.out_of_countr" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</span>
                    <span v-show="!assessment.out_of_countr" class="badge badge-danger badge-pill" style="font-size: 1.5em;">No</span>
                  </div>
                  <div v-else>
                    <b-button @click="assessment.out_of_countr = false;calRL(assessment)" v-show="assessment.out_of_countr" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</b-button>
                    <b-button @click="assessment.out_of_countr = true;calRL(assessment)" v-show="!assessment.out_of_countr" class="badge badge-danger badge-pill" style="font-size: 1.5em;">No</b-button>
                  </div>
                </b-col>
              </b-row>
              <hr>
              <b-row class="mb-3">
                <b-col><label for="most_recent_test_failure"><strong>Most Recent Test Failure</strong></label></b-col>
              </b-row>
            </div>
            <b-button type="submit" v-show="assessment.edit" variant="outline-success" class="m-2" v-on:click="toggleEditAssessment(assessment)">Save</b-button>
          </b-card-body>
        </b-card>
      </div>
      <div class="d-flex justify-content-center m-3">
        <b-button v-show="!show_assessments" @click="show_assessments = true" class="m-1" variant="light">View All Assessments</b-button>
        <b-button v-show="show_assessments" @click="show_assessments = false" class="m-1" variant="light">Hide Assessments</b-button>
      </div>
    </b-collapse>
    <div class="d-flex my-3">
      <div v-show="edit">
        <b-button variant="outline-info" class="m-2" v-on:click="add_assessment()" v-show="!added_risk_assessment">New Assessment</b-button>
        <b-button variant="outline-danger" class="m-2" v-on:click="cancel()">Cancel</b-button>
      </div>
    </div>
  </div>
</template>

<script>
import { cloneDeep } from 'lodash'
import riskAssessment from './orgRiskAssessmentTemp.js'
import { CustomRequest, genTempKey } from '../../common/CustomRequest.js'
import vSelect from 'vue-select'

export default {
  name: 'SupplierRiskAssessments',
  components: {
    vSelect
  },
  props: {
    doc: {
      required: true,
      type: Object
    },
    id: {
      required: true,
      type: Number
    },
    orgName: {
      required: true,
      type: String
    },
    timestampFetched: {
      required: true,
      type: String
    }
  },
  data () {
    return {
      edit: false,
      doc_buffer: {},
      added_risk_assessment: null,
      show_assessments: false,
      del_url_previews: [],
      req: new CustomRequest(this.$cookies.get('session'))
    }
  },
  computed: {
    num_risk_assessments: function () {
      return this.doc_buffer.supplier_risk_assessments.length
    }
  },
  methods: {
    toggleEditAssessment: function (assessment) {
      if (assessment.edit) {
        assessment.user_edit_history.push({
          user: {
            department: this.$root.userData.department,
            first_name: this.$root.userData.first_name,
            last_name: this.$root.userData.last_name,
            organization_id: this.$root.userData.organization_id,
            person_id: this.$root.userData.person_id,
            user_id: this.$root.userData.user_id,
            user_name: this.$root.userData.user_name,
            profile_picture: this.$root.userData.profile_picture
          },
          date: new Date().toISOString(),
          action: 'Edited'
        })
        this.calRL(assessment)
        this.submit()
      }
      assessment.edit = !assessment.edit
    },
    deleteDocument: function (documents, document) {
      this.$bvModal.msgBoxConfirm(`Are you sure you want to perminently delete '${document.name}' document?`).then(value => {
        if (value) {
          documents.splice(documents.findIndex((d) => d.id === document.id), 1)
          console.log(document.file_hash)
          this.req.deleteFile(document.file_hash)
        }
      })
    },
    addDocument: function (documents, assessmentNum) {
      const document = {
        id: genTempKey(),
        description: null,
        name: null,
        document_type: null,
        type: `supplier_risk_assessments/assesment${assessmentNum}`,
        id_code: `${this.orgName}_${this.id}_`,
        file_pointer: null,
        file_preview_pointer: null,
        file_type: null,
        url_preview: null,
        file_hash: null,
        date_uploaded: null
      }
      documents.unshift(document)
    },
    calRL: function (assessment) {
      assessment.risk_level_granted = 'High_Risk'
      if (
        assessment.supplier_questionnaire.satisfactory &&
        assessment.provides_cofas &&
        assessment.provides_spec_sheets &&
        !assessment.most_recent_test_failure.failed_test
      ) {
        assessment.risk_level_granted = 'Medium_Risk'
      }
      if (
        assessment.supplier_questionnaire.satisfactory &&
        assessment.supplier_certs.satisfactory &&
        assessment.food_safety_plan.satisfactory &&
        assessment.provides_cofas &&
        assessment.provides_spec_sheets &&
        !assessment.most_recent_test_failure.failed_test
      ) {
        assessment.risk_level_granted = 'Low_Risk'
      }
    },
    calRLs: function () {
      for (let i = 0; i < this.doc_buffer.supplier_risk_assessments.length; i++) {
        this.calRL(this.doc_buffer.supplier_risk_assessments[i])
      }
    },
    toggleEdit: function () {
      this.edit = !this.edit
      this.$emit('editRiskAssessment', this.edit)
    },
    getFile: function (document) {
      if (document.file_hash) {
        const url = this.$root.getOrigin() + '/api/v1/uploads/' + document.file_pointer
        return url
      } else {
        return document.url_preview
      }
    },
    onFileChange: async function (e, document) {
      if (e.target.files.length === 0) {
        return
      }

      // Preview File
      const file = e.target.files[0]
      document.date_uploaded = new Date().toISOString()
      document.id_code += document.document_type
      document.url_preview = URL.createObjectURL(file)
      this.del_url_previews.push(file)

      const customKey = await this.req.addFile(file, 1, document.id_code, document.type)
      document.file_pointer = customKey
    },
    cancel: function () {
      this.toggleEdit()
      this.$emit('toggleLoaded', false)
      this.$emit('refreshParent')
      this.doc_buffer.supplier_risk_assessments.forEach(assessment => {
        assessment.edit = false
      })
    },
    initials: function (userData) {
      const f = Array.from(userData.first_name)[0]
      const l = Array.from(userData.last_name)[0]
      const i = f + l
      return i
    },
    add_assessment: function () {
      const ra = cloneDeep(riskAssessment)
      ra.risk_assesment_id = this.num_risk_assessments + 1
      ra.assessment_date = new Date().toLocaleDateString()
      ra.modified_date = new Date().toLocaleDateString()
      ra.user_edit_history.push({
        user: {
          department: this.$root.userData.department,
          first_name: this.$root.userData.first_name,
          last_name: this.$root.userData.last_name,
          organization_id: this.$root.userData.organization_id,
          person_id: this.$root.userData.person_id,
          user_id: this.$root.userData.user_id,
          user_name: this.$root.userData.user_name,
          profile_picture: this.$root.userData.profile_picture
        },
        date: new Date().toISOString(),
        action: 'Created'
      })
      ra.edit = true
      this.added_risk_assessment = this.num_risk_assessments + 1
      this.doc_buffer.current_supplier_risk_assesment_id = this.num_risk_assessments + 1
      this.doc_buffer.supplier_risk_assessments.unshift(ra)
    },
    submit: async function () {
      const createToast = this.$root.createToast
      this.$emit('toggleLoaded', false)

      this.doc_buffer.supplier_risk_assessments.forEach(assessment => {
        assessment.edit = false
      })

      for (let i = 0; i < this.doc_buffer.length; i++) {
        delete this.doc_buffer[i].edit
      }

      const updateOrg = {
        organization_id: this.id,
        risk_level: this.doc_buffer.supplier_risk_assessments[0].risk_level_granted,
        doc: this.doc_buffer,
        timestamp_fetched: this.timestampFetched
      }
      if (this.doc_buffer.supplier_risk_assessments[0].risk_level_granted === 'Low_Risk') {
        updateOrg.vetted = true
        updateOrg.date_vetted = new Date().toISOString()
      }

      this.req.upsertRecord('Organizations', updateOrg)

      const resp = await this.req.sendRequest(this.$root.getOrigin())

      resp.messages.flash.forEach(message => {
        createToast(message)
      })

      if (resp.status === 201) {
        this.req = new CustomRequest(this.$cookies.get('session'))
        this.edit = false
        this.$parent.edit_supplier_risk_assessment = false
        this.$parent.refreshParent()
        this.del_url_previews.forEach(url => URL.revokeObjectURL(url))
        return true
      }
      this.$root.handleStaleRequest(this.req.isStale(), window.location)
      this.$emit('toggleLoaded', true)
      this.edit = true
      this.$parent.edit_supplier_risk_assessment = true
      return false
    }
  },
  watch: {
    doc_buffer: function () {
      this.calRLs()
    }
  },
  created: function () {
    this.doc_buffer = cloneDeep(this.doc)
    this.doc_buffer.supplier_risk_assessments.forEach(assessment => {
      assessment.edit = false
    })
  }
}
</script>

<style>
.card {
  box-shadow: 0 2px 2px rgba(0,0,0,.2);
}
</style>

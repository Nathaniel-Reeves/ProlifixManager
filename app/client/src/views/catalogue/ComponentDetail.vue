<template>
  <div class="my_component d-flex flex-wrap justify-content-center">
    <div class="card my-2" v-if="!loaded">
      <div class="card-body">
        <div class="d-flex justify-content-center">
          <div class="spinner-border text-primary" role="status"></div>
        </div>
      </div>
    </div>

    <b-container fluid class="p-0">
      <b-card class=" my-2" v-if="loaded">
        <b-card-body>
          <div class="card-title d-flex align-items-center flex-wrap">
            <b-img style="max-width: 15rem;" class="d-none d-print-inline p-2" src="../../assets/Company Images/logos jpg/Cropped Logo.jpg"></b-img>
            <h2 class="card-title">{{ get_comopnent_primary_name(component_data) }} {{ format_string(component_data.component_type) }}</h2>
            <CertBadge :data="component_data"></CertBadge>
          </div>
          <hr class="d-print-none">
          <b-nav pills card-header slot="header" v-b-scrollspy:nav-scroller class="text-nowrap d-print-none">
            <b-nav-item href="#Aliases" @click="scrollIntoView">Aliases</b-nav-item>
            <b-nav-item href="#Specifications" @click="scrollIntoView"
              v-if="component_data.doc.specifications !== undefined">Specifications</b-nav-item>
            <div v-for="(spec, spec_key) in component_data.doc.specifications.specs" :key="spec_key">
              <b-nav-item :href="'#'+spec_key" @click="scrollIntoView">{{ spec.test_name }}</b-nav-item>
            </div>
          </b-nav>
        </b-card-body>
      </b-card>

      <b-card class=" my-2" v-if="loaded">
        <b-card-body id="nav-scroller" ref="content" class="scrollbox">

          <!-- Alias Names -->
          <NamesComponent :data="component_data.Component_Names" :save-function="putComponent" naming-type="component" :allow-edit="true">
          </NamesComponent>
          <hr>

          <!-- Specifications -->
          <div v-if="component_data.doc.specifications !== undefined">
            <h3 id="Specifications">Specifications<b-button v-if="!edit_specs" v-b-tooltip.hover title="Edit Component Specifications" v-on:click="editSpecs()" class="btn p-1 ml-2 btn-light" type="button"><b-icon icon="pencil-square" class="d-print-none"></b-icon></b-button></h3>
            <div v-if="!edit_specs">
              <p><strong>Spec Issued: </strong>{{ component_data.doc.specifications.date_issued !== undefined && component_data.doc.specifications.date_issued !== '' ? new Date(component_data.doc.specifications.date_issued).toDateString() : "No Spec" }}</p>
              <p><strong>Spec Revised: </strong>{{ component_data.doc.specifications.date_revised !== undefined && component_data.doc.specifications.date_revised !== '' ? new Date(component_data.doc.specifications.date_revised).toDateString() : "No Spec" }}</p>
              <p><strong>Revision Number: </strong>{{ component_data.doc.specifications.revision_number }}</p>
            </div>
            <div v-if="!edit_specs">
              <p v-if="component_data.doc.specifications.description_statement.length > 0"><strong>Component Description</strong><br>{{ component_data.doc.specifications.description_statement }}</p>
              <p v-if="component_data.doc.specifications.origin.length > 0"><strong>Origin</strong><br>{{ component_data.doc.specifications.origin }}</p>
              <p v-if="component_data.doc.specifications.identity_statement.length > 0"><strong>Identity Statement</strong><br>{{ component_data.doc.specifications.identity_statement }}</p>
              <p v-if="component_data.doc.specifications.strength_statement.length > 0"><strong>Strength Statement</strong><br>{{ component_data.doc.specifications.strength_statement }}</p>
              <p v-if="component_data.doc.specifications.purity_statement.length > 0"><strong>Purity Statement</strong><br>{{ component_data.doc.specifications.purity_statement }}</p>
              <p v-if="component_data.doc.specifications.parts_used.length > 0"><strong>Parts Used</strong><br>{{ component_data.doc.specifications.parts_used }}</p>
            </div>
            <div v-if="edit_specs">
              <b-form-group>
                <label for="description_statement"><strong>Component Description</strong><br></label>
                <b-form-textarea id="description_statement" v-model="edit_specs_buffer.description_statement" placeholder="Component description..." rows="3" max-rows="6"></b-form-textarea>
                <label for="origin"><strong>Origin</strong><br></label>
                <b-form-textarea id="origin" v-model="edit_specs_buffer.origin" placeholder="Component origin..." rows="3" max-rows="6"></b-form-textarea>
                <label for="identity_statement"><strong>Identity Statement</strong><br></label>
                <b-form-textarea id="identity_statement" v-model="edit_specs_buffer.identity_statement" placeholder="Component identity statement..." rows="3" max-rows="6"></b-form-textarea>
                <label for="strength_statement"><strong>Strength Statement</strong><br></label>
                <b-form-textarea id="strength_statement" v-model="edit_specs_buffer.strength_statement" placeholder="Component strength statement..." rows="3" max-rows="6"></b-form-textarea>
                <label for="purity_statement"><strong>Purity Statement</strong><br></label>
                <b-form-textarea id="purity_statement" v-model="edit_specs_buffer.purity_statement" placeholder="Component purity statement..." rows="3"  max-rows="6"></b-form-textarea>
                <label for="parts_used"><strong>Parts Used</strong><br></label>
                <b-form-textarea id="parts_used" v-model="edit_specs_buffer.parts_used" placeholder="Parts used..." rows="1"  max-rows="2"></b-form-textarea>
              </b-form-group>
              <div class="d-flex">
                <b-button v-if="edit_specs" variant="outline-info" class="m-2" v-on:click="cancelEditSpecs()">Cancel</b-button>
                <b-button type="submit" v-if="edit_specs" variant="primary" class="m-2" v-on:click="editSpecs()">Save</b-button>
              </div>
            </div>

            <hr>

            <!-- Generic Specifications -->
            <div v-for="(spec, spec_key, index) in component_data.doc.specifications.specs" :key="index" style="break-inside: avoid;">

              <h3 :id="spec_key">{{ spec.test_name }}<b-button v-if="!edit_specs" v-b-tooltip.hover :title="'Edit Component ' + spec.test_name + ' Specifications'" v-on:click="editSpecs()" class="btn p-1ml-2 btn-light" type="button"><b-icon icon="pencil-square" class="d-print-none"></b-icon></b-button></h3>
              <div v-if="!edit_specs">
                <p v-if="spec_key != 'example_cofas'"><strong>Spec Issued: </strong>{{ spec.date_issued !== undefined && spec.date_issued !== '' ? new Date(spec.date_issued).toDateString() : "No Spec" }}</p>
                <p v-if="spec_key != 'example_cofas'"><strong>Spec Revised: </strong>{{ spec.date_revised !== undefined && spec.date_revised !== '' ? new Date(spec.date_revised).toDateString() : "No Spec" }}</p>
                <p v-if="spec_key != 'example_cofas'"><strong>Revision Number: </strong>{{ spec.revision_number }}</p>
                <p v-if="spec_key != 'example_cofas'"><strong>Accepted Testing Sources: </strong>
                  <b-badge variant="secondary" pill class="ml-2" style="font-size:1em;" v-show="spec.locations.in_house">In House</b-badge>
                  <b-badge variant="secondary" pill class="ml-2" style="font-size:1em;" v-show="spec.locations.third_party_lab">Third Party Lab</b-badge>
                  <b-badge variant="secondary" pill class="ml-2" style="font-size:1em;" v-show="spec.locations.supplier">Supplier</b-badge>
                </p>
                <p v-if="spec_key != 'example_cofas'"><strong>Primary Testing Responsibility: </strong>
                  <b-badge variant="primary" pill class="ml-2" style="font-size:1em;">{{ format_string(spec.locations.primary) }}</b-badge>
                </p>
                <p v-if="spec_key != 'example_cofas'"><strong>Spec Required: </strong><b-badge pill class="ml-2" style="font-size:1em;" v-bind:variant="(spec.required_spec ? 'success' : 'warning')">{{ spec.required_spec ? 'YES' : 'NO' }}</b-badge></p>
                <p v-show="Boolean(spec.statement)"><strong>Statement</strong><br>{{ spec.statement }}</p>
              </div>

              <div v-if="edit_specs && spec_key != 'example_cofas'">
                <b-form-group>
                  <label :for="'spec_accepted_' + spec_key"><strong>Accepted Test Sources: <br></strong></label>
                  <b-form-checkbox :name="'spec_accepted_' + spec_key" v-model="edit_specs_buffer.specs[spec_key].locations.in_house">In House</b-form-checkbox>
                  <b-form-checkbox :name="'spec_accepted_' + spec_key" v-model="edit_specs_buffer.specs[spec_key].locations.third_party_lab">Third Party Lab</b-form-checkbox>
                  <b-form-checkbox :name="'spec_accepted_' + spec_key" v-model="edit_specs_buffer.specs[spec_key].locations.supplier">Supplier</b-form-checkbox>
                </b-form-group>

                <b-form-group v-model="edit_specs_buffer.specs[spec_key].locations.primary">
                  <label :for="'spec_responsibility_' + spec_key"><strong>Primary Testing Responsibility: </strong></label>
                  <b-form-radio v-model="edit_specs_buffer.specs[spec_key].locations.primary" :name="'spec_responsibility_' + spec_key" value="in_house">In House</b-form-radio>
                  <b-form-radio v-model="edit_specs_buffer.specs[spec_key].locations.primary" :name="'spec_responsibility_' + spec_key" value="third_party_lab">Third Party Lab</b-form-radio>
                  <b-form-radio v-model="edit_specs_buffer.specs[spec_key].locations.primary" :name="'spec_responsibility_' + spec_key" value="supplier">Supplier</b-form-radio>
                </b-form-group>

                <div class="d-flex">
                  <label :for="'spec_required_' + spec_key"><strong>Spec Required: </strong></label>
                  <b-form-checkbox class="ml-2" v-model="edit_specs_buffer.specs[spec_key].required_spec" :name="'spec_required_' + spec_key" switch>
                      <b-badge class="ml-2" style="font-size:1em;" pill v-bind:variant="(edit_specs_buffer.specs[spec_key].required_spec ? 'success' : 'warning')">{{ edit_specs_buffer.specs[spec_key].required_spec ? 'YES' : 'NO' }}</b-badge>
                  </b-form-checkbox>
                </div>
                <label :for="'statement_' + spec_key"><strong>Statement</strong><br></label>
                <b-form-textarea class="d-flex" :id="'statement_' + spec_key" v-model="edit_specs_buffer.specs[spec_key].statement" placeholder="Statement..." rows="3" max-rows="6"></b-form-textarea>
              </div>

              <div>
                <div v-if="!edit_specs">
                  <b-card-group deck v-if="useCardType(spec_key)">
                    <div v-for="test, test_key, index in spec.tests" :key="index">
                      <b-card no-body style="max-width: 25rem;" class="my-3 no-shaddow d-print-block">
                        <b-link :href="getFile(test.file_pointer)" target="_blank"><b-card-img
                            v-if="(spec_key === 'microscopic' || spec_key === 'organoleptic') && getFile(test.file_pointer)"
                            :src="getFile(test.file_pointer)" top></b-card-img></b-link>
                        <b-card-body v-if="spec_key === 'microscopic'">
                          <b-card-title>{{ test.id_code }}</b-card-title>
                          <b-card-text>
                            <p class="mb-2">{{ test.statement }}</p>
                            <strong>Magnification: </strong><b-badge variant="secondary" pill class="ml-2" style="font-size:1em;">{{
                              test.magnification }}</b-badge><br>
                            <strong>Method: </strong>{{ test.method }}
                          </b-card-text>
                        </b-card-body>
                        <b-card-body v-else-if="spec_key === 'organoleptic'">
                          <b-card-title>{{ test.id_code }}</b-card-title>
                          <b-card-text>
                            <p><strong>Odor: </strong><br>{{ test.odor }}</p>
                            <p><strong>Dissolved Taste: </strong><br>{{ test.taste_dissolved }}</p>
                            <p><strong>Dry Taste: </strong><br>{{ test.taste_dry }}</p>
                            <p><strong>Visual: </strong><br>{{ test.visual }}</p>
                          </b-card-text>
                        </b-card-body>
                        <b-card-body v-else-if="spec_key === 'example_cofas'">
                          <b-card-title>{{ test.id_code }}</b-card-title>
                          <b-card-text>
                            <p><strong>Notes: </strong><br>{{ test.statement }}</p>
                            <b-button :href="getFile(test.file_pointer)" target="_blank" class="btn-light">View CofA</b-button>
                          </b-card-text>
                        </b-card-body>
                        <b-card-body v-else>
                          <b-card-title>{{ test.id_code }}</b-card-title>
                        </b-card-body>
                        <b-card-footer>{{ new Date(test.date_revised).toDateString() }}</b-card-footer>
                      </b-card>
                    </div>
                  </b-card-group>

                  <div v-else>
                    <!-- <Grid v-show="spec.tests.length > 0" :rows="spec.tests" :cols="test_cols"></Grid> -->
                    <Vue3EasyDataTable :headers="headers" :items="spec.tests" hide-footer table-class-name="customize-table">
                      <template #item-test_name="{ test_name }">
                        {{ test_name }}
                      </template>
                      <template #item-required_spec="{ required_spec }">
                        <span v-if="required_spec" class="badge badge-success badge-pill" style="font-size: 1em;">Yes</span>
                        <span v-else class="badge badge-warning badge-pill" style="font-size: 1em;">No</span>
                      </template>
                      <template #item="{ item }">
                        {{ item.inequality === '=' ? '' : item.inequality }}{{ item.count.toLocaleString() }} {{ item.unit_of_measure }}
                      </template>
                      <template #item-methods="{ methods }">
                        <!-- {{ methods.join(', ') }} -->
                        <div v-for="method in methods" :key="method">
                          {{ method }}
                        </div>
                      </template>
                      <template #item-statement="{ statement }">
                        {{ statement }}
                      </template>
                      <template #empty-message>
                        <p>No Specs</p>
                      </template>
                    </Vue3EasyDataTable>
                  </div>
                </div>

                <div v-if="edit_specs">
                  <b-card-group deck v-if="useCardType(spec_key)">
                    <div v-for="( test, index ) in edit_specs_buffer.specs[spec_key].tests" :key="index">
                      <b-card no-body style="max-width: 25rem; min-width: 25rem;" class="my-3">
                        <b-card-img :src="test.url_preview || test.url_preview === null ? test.url_preview : getFile(test.file_pointer)"
                          top></b-card-img>
                        <b-card-body v-if="spec_key === 'microscopic'">
                          <b-form-file no-drop required accept="image/png, image/jpeg"
                            v-show="!test.url_preview && !test.file_pointer && test.id_code !== null && test.id_code.length > 3" type="file"
                            class="my-2" @change="onFileChange($event, test)"></b-form-file>
                          <b-form-input v-show="!test.file_pointer" type="text" class="my-1" v-model="test.id_code"
                            placeholder="Lot Number..."></b-form-input>
                          <b-card-title v-show="test.file_pointer && test.id_code !== null && test.id_code.length > 3" class="my-1">{{ test.id_code
                            }}</b-card-title>
                          <strong>Discription: </strong><br><b-form-textarea class="my-1" rows="3" max-rows="3" v-model="test.statement"
                            placeholder="Discription..."></b-form-textarea>
                          <strong>Magnification: </strong><br><b-form-select v-model="test.magnification" required
                            :options="[{ value: '', text: 'Select Magnification' },{ value: '20X', text: '20X' },{ value: '40X', text: '40X' }]"></b-form-select>
                          <strong>Method: </strong><br><b-form-select v-model="test.method" required
                            :options="[{ value: '', text: 'Select Method' }, { value: 'SOP QA 04.02', text: 'SOP QA 04.02' }]"></b-form-select>
                        </b-card-body>
                        <b-card-body v-if="spec_key === 'example_cofas'">
                          <strong>Lot #: </strong><br><b-form-input v-show="!test.file_pointer" type="text" class="my-1" v-model="test.id_code"
                            placeholder="Lot Number..."></b-form-input>
                          <b-card-title v-show="test.file_pointer && test.id_code !== null && test.id_code.length > 3" class="my-1">{{ test.id_code
                            }}</b-card-title>
                          <strong>Notes: </strong><br><b-form-textarea class="my-1" rows="3" max-rows="3" v-model="test.statement"
                            placeholder="Notes..."></b-form-textarea>
                          <b-form-file no-drop required accept="image/png, image/jpeg, application/pdf"
                            :disabled="test.id_code === null || test.id_code === '' || test.id_code.length < 3" type="file" class="my-2"
                            @change="onFileChange($event, test)"></b-form-file>
                        </b-card-body>
                        <b-card-body v-if="spec_key === 'organoleptic'">
                          <b-form-file no-drop required accept="image/png, image/jpeg"
                            v-show="!test.url_preview && !test.file_pointer && test.id_code !== null && test.id_code.length > 3" type="file"
                            class="my-2" @change="onFileChange($event, test)"></b-form-file>
                          <b-form-input v-show="!test.file_pointer" type="text" class="my-1" v-model="test.id_code"
                            placeholder="Lot Number..."></b-form-input>
                          <b-card-title v-show="test.file_pointer && test.id_code !== null && test.id_code.length > 3" class="my-1">{{ test.id_code
                            }}</b-card-title>
                          <strong>Odor: </strong><br><b-form-textarea class="my-1" rows="2" max-rows="2" v-model="test.odor"
                            placeholder="Odor..."></b-form-textarea>
                          <strong>Dissolved Taste: </strong><br><b-form-textarea class="my-1" rows="2" max-rows="2" v-model="test.taste_dissolved"
                            placeholder="Dissolved Taste..."></b-form-textarea>
                          <strong>Dry Taste: </strong><br><b-form-textarea class="my-1" rows="2" max-rows="2" v-model="test.taste_dry"
                            placeholder="Dry Taste..."></b-form-textarea>
                          <strong>Visual: </strong><br><b-form-textarea class="my-1" rows="2" max-rows="2" v-model="test.visual"
                            placeholder="Visual..."></b-form-textarea>
                          <strong>Method: </strong><br><b-form-select v-model="test.method" required
                            :options="[{ value: '', text: 'Select Method' }, { value: 'SOP QA 04.02', text: 'SOP QA 04.01' }]"></b-form-select>
                        </b-card-body>
                        <b-card-footer>
                          <b-button class="my-2" variant="outline-danger" @click="removeTest(index, spec_key)">Remove</b-button>
                        </b-card-footer>
                      </b-card>
                    </div>
                    <b-card v-if="spec_key === 'microscopic'" img-src="../../assets/no_image_placeholder.png" class="my-3"
                      style="max-width: 25rem; min-width: 25rem; cursor: pointer;" v-on:click="newCardSpec(spec_key)">
                      <b-card-title>New Microscopic Image</b-card-title>
                    </b-card>
                    <b-card v-else-if="spec_key === 'organoleptic'" class="my-3" style="max-width: 25rem; min-width: 25rem; cursor: pointer;"
                      v-on:click="newCardSpec(spec_key)">
                      <b-card-title>New Organoleptic Spec</b-card-title>
                    </b-card>
                  </b-card-group>

                  <div v-else>
                    <h5 class="mt-4">Individual Specifications</h5>
                    <div v-for="( test, index ) in edit_specs_buffer.specs[spec_key].tests" :key="index">
                      <b-form inline class="d-flex mt-4 mb-2" style="align-items: baseline;">
                        <label class="sr-only" for="test">Test</label>
                        <b-form-input id="test" class="bold mr-sm-2" style="width:30%; min-width: 15rem;" placeholder="Test..."
                          v-model="test.test_name" v-b-tooltip.hover title="Test Name"></b-form-input>
                        <label class="sr-only">Spec Required</label>
                        <b-form-checkbox v-model="test.required_spec" class="mr-sm-2" style="font-size:1em;" pill
                          v-bind:button-variant="(test.required_spec ? 'success' : 'warning')" button v-b-tooltip.hover title="Required Spec">
                          <strong>{{ test.required_spec ? 'YES' : 'NO' }}</strong>
                        </b-form-checkbox>
                        <b-form-radio-group v-model="test.inequality" class="mr-2" buttons button-variant="outline-info">
                          <b-form-radio value=">">&#62;</b-form-radio>
                          <b-form-radio value="=">&#61;</b-form-radio>
                          <b-form-radio value="<">&#60;</b-form-radio>
                        </b-form-radio-group>
                        <label class="sr-only" for="spec">Spec</label>
                        <b-input-group class="mr-sm-2">
                          <b-form-input style="width:15%;" id="spec" placeholder="Spec..." v-b-tooltip.hover title="Specification" type="number"
                            min="0" no-wheel number v-model="test.count"></b-form-input>
                        </b-input-group>
                        <b-form-select v-model="test.unit_of_measure" :options="['%','cfu/g','cfu/10g','cfu/25g','ppm','rf']" class="mr-sm-2"
                          placeholder="Select Units"></b-form-select>
                      </b-form>
                      <b-form-tags v-model="test.methods" no-outer-focus class="mb-2" style="width:86%;">
                        <template v-slot="{ tags, inputAttrs, inputHandlers, addTag, removeTag }">
                          <b-input-group class="mb-2">
                            <b-form-input v-bind="inputAttrs" v-on="inputHandlers" placeholder="New Method - Press enter to add"
                              class="form-control"></b-form-input>
                            <b-input-group-append>
                              <b-button @click="addTag()" variant="outline-primary">Add</b-button>
                            </b-input-group-append>
                          </b-input-group>
                          <div class="d-inline-block" style="font-size: 1.5rem;">
                            <b-form-tag v-for="tag in tags" @remove="removeTag(tag)" :key="tag" :title="tag" variant="light" class="mr-1">{{ tag
                              }}</b-form-tag>
                          </div>
                        </template>
                      </b-form-tags>
                      <b-form inline class="d-flex mb-4" style="align-items: end;">
                        <b-form-textarea class="mb-2 mr-sm-2" style="width:80%;" v-model="test.statement" placeholder="Statement..." rows="2"
                          max-rows="3"></b-form-textarea>
                        <b-button class="mb-2 mr-sm-2" variant="outline-danger" @click="removeTest(index, spec_key)">Remove</b-button>
                      </b-form>
                    </div>
                  </div>
                </div>
              </div>

              <div class="d-flex mt-3" v-if="edit_specs">
                <b-button v-show="spec_key !== 'microscopic'" variant="outline-info" class="m-2" v-on:click="addSpec(spec_key)">{{spec_key !=
                  'example_cofas'? 'New Spec':'New CofA'}}</b-button>
                <b-button v-if="edit_specs" variant="outline-info" class="m-2" v-on:click="cancelEditSpecs()">Cancel</b-button>
                <b-button type="submit" v-if="edit_specs" variant="primary" class="m-2" v-on:click="editSpecs(spec_key)">Save</b-button>
              </div>
              <hr>
            </div>
          </div>

        </b-card-body>
      </b-card>
    </b-container>
  </div>
</template>

<style scoped>
.scrollbox {
  position:relative;
  height:85vh;
  overflow-y:scroll;
}
.customize-table {
  --easy-table-body-item-padding:10px 10px 10px 10px;
}
@media print {
  .scrollbox {
    height: 100%;
    overflow-y:auto;
  }
  @page {
    margin: 30mm 30mm 10mm 10mm;
  }
  body {
    margin: 0px;
  }
}
.bold {
    font-weight: bold;
}
.my_component {
    width: 95%;
}
@media (max-width: 1024px) {
    .my_component {
        width: 98%;
    }
}
@media (max-width: 400px) {
    .my_component {
        width: 100%;
    }
}
</style>

<script>
import NamesComponent from './NamesComponent.vue'
import CertBadge from '../../components/CertBadge.vue'
import Vue3EasyDataTable from 'vue3-easy-data-table'

export default {
  name: 'ComponentDetail',
  components: {
    NamesComponent,
    CertBadge,
    Vue3EasyDataTable
  },
  data: function () {
    return {
      id: this.$route.params.id,
      component_data: {},
      search_query: '',
      loaded: false,
      headers: [
        { text: 'Test', value: 'test_name', width: 250 },
        { text: 'Rqd', value: 'required_spec', width: 30 },
        { text: 'Spec', value: 'generated', width: 80 },
        { text: 'Methods', value: 'methods', width: 110 },
        { text: 'Statement', value: 'statement', width: 250 }
      ],
      edit_names: false,
      edit_names_buffer: [],
      edit_specs: false,
      edit_specs_buffer: {},
      upload_files_buffer: {},
      remove_files_buffer: [],
      flash_messages: [],
      file_index: 1
    }
  },
  methods: {
    addSpec: function (specKey) {
      const test = this.newTest()
      test.type = 'component_specifications/' + specKey
      this.edit_specs_buffer.specs[specKey].tests.push(test)
    },
    newCardSpec: function (specKey) {
      const test = this.newTest()
      test.test_name = this.edit_specs_buffer.specs[specKey].test_name
      test.type = 'component_specifications/' + specKey
      test.required_spec = this.edit_specs_buffer.specs[specKey].required_spec
      this.edit_specs_buffer.specs[specKey].tests.push(test)
    },
    removeTest: function (index, specKey) {
      for (const pair in this.upload_files_buffer) {
        if (this.edit_specs_buffer.specs[specKey].tests[index].file_pointer === pair[0]) {
          this.upload_files_buffer.splice(pair[0], 1)
        }
      }
      if (this.edit_specs_buffer.specs[specKey].tests[index].file_hash) {
        this.remove_files_buffer.push(this.edit_specs_buffer.specs[specKey].tests[index].file_hash)
      }
      this.edit_specs_buffer.specs[specKey].tests.splice(index, 1)
    },
    newTest: function () {
      const today = new Date().toISOString()
      return {
        test_name: null,
        type: null,
        summary: null,
        statement: null,
        description: null,
        magnification: null,
        required_spec: true,
        method: null,
        methods: [],
        unit_of_measure: '',
        count: 0,
        greater_than: false,
        less_than: true,
        sources: [],
        odor: null,
        taste_dissolved: null,
        taste_dry: null,
        visual: null,
        id_code: null,
        file_pointer: null,
        file_preview_pointer: null,
        date_issued: today,
        date_revised: today,
        url_preview: null
      }
    },
    getFile: function (filename) {
      if (filename) {
        const url = window.origin + '/api/v1/uploads/' + filename
        return url
      } else {
        return ''
      }
    },
    useCardType: function (specKey) {
      const cardTypes = [
        'organoleptic',
        'microscopic',
        'ftir',
        'hplc',
        'hptlc',
        'example_cofas'
      ]
      return cardTypes.includes(specKey)
    },
    onFileChange: function (e, test) {
      // Preview File
      const file = e.target.files[0]
      test.url_preview = URL.createObjectURL(file)
      URL.revokeObjectURL(file)

      // Save File in Buffer
      const newFile = {
        filename: this.get_comopnent_primary_name(this.component_data),
        type: test.type,
        page: 1,
        id_code: test.id_code,
        file: file
      }

      const customKey = 'file_' + this.file_index
      const obj = {}
      obj[customKey] = newFile
      Object.assign(this.upload_files_buffer, obj)
      test.file_pointer = customKey
      this.file_index += 1
    },
    editSpecs: function (subSpec) {
      const original = structuredClone(this.component_data.doc.specifications) // Deep Copy
      if (!this.edit_specs) {
        this.edit_specs_buffer = structuredClone(this.component_data.doc.specifications) // Deep Copy
        this.edit_specs = true
      } else {
        this.component_data.doc.specifications = {}
        if (this.edit_specs_buffer.revision_number === 0) {
          this.edit_specs_buffer.date_issued = new Date().toISOString() // Today
        }
        this.edit_specs_buffer.revision_number++
        this.edit_specs_buffer.date_revised = new Date().toISOString() // Today
        if (subSpec !== undefined) {
          if (this.edit_specs_buffer.specs[subSpec].revision_number === 0) {
            this.edit_specs_buffer.specs[subSpec].date_issued = new Date().toISOString() // Today
          }
          this.edit_specs_buffer.specs[subSpec].revision_number++
          this.edit_specs_buffer.specs[subSpec].date_revised = new Date().toISOString() // Today
        }
        this.component_data.doc.specifications = structuredClone(this.edit_specs_buffer) // Deep Copy
        this.component_data.doc.files = structuredClone(this.upload_files_buffer)
        this.putComponent().then(outcome => {
          if (outcome === true) {
            this.edit_specs_buffer = []
            this.upload_files_buffer = {}
            this.remove_files_buffer = []
            this.edit_specs = false
          } else {
            this.component_data.doc.specifications = original
          }
        })
      }
    },
    cancelEditSpecs: function () {
      this.edit_specs_buffer = []
      this.edit_files_buffer = {}
      this.remove_files_buffer = []
      this.edit_specs = false
    },
    scrollIntoView: function (event) {
      event.preventDefault()
      const href = event.target.getAttribute('href')
      const el = href ? document.querySelector(href) : null
      if (el) {
        this.$refs.content.scrollTop = el.offsetTop
      }
    },
    format_string: function (type) {
      if (type === undefined) {
        return ''
      }
      return type.toLowerCase().split('_').map((s) => s.charAt(0).toUpperCase() + s.substring(1)).join(' ')
    },
    get_comopnent_primary_name: function (component) {
      if (component.Component_Names !== undefined && component.Component_Names.length > 0) {
        for (let i = 0; i < component.Component_Names.length; i++) {
          if (component.Component_Names[i].primary_name) {
            return component.Component_Names[i].component_name
          }
        }
      }
      return 'No Name'
    },
    getComponentData: function () {
      const fetchRequest = window.origin + '/api/v1/catalogue/components?component-id=' + this.id + '&populate=product_materials&populate=purchase_order_detail&populate=item_id&populate=inventory&populate=brand&doc=true'
      // eslint-disable-next-line
      console.log(
        'GET ' + fetchRequest
      )
      fetch(fetchRequest, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include'
      }).then(response => {
        if (response.status === 200) {
          response.json().then(data => {
            this.component_data = Object.values(data.data[0])[0]
            if (this.component_data.doc === null) {
              this.component_data.doc = {}
            }
            // eslint-disable-next-line
            console.log(this.component_data)
            this.loaded = true
          })
        } else if (response.status === 404) {
          this.$router.push({ path: '/404' })
        } else if (response.status === 401) {
          this.$router.push({
            name: 'login'
          })
        } else {
          // eslint-disable-next-line
          console.log('Looks like there was a problem. Status Code:' + response.status)
          // eslint-disable-next-line
          console.log(response)
        }
      })
    },
    putComponent: async function () {
      const fetchRequest = window.origin + '/api/v1/catalogue/components'
      // eslint-disable-next-line
      console.log(
        'PUT ' + fetchRequest
      )
      const formData = new FormData()
      formData.append('component_id', this.id)
      formData.append('component_type', this.component_data.component_type)
      formData.append('certified_usda_organic', this.component_data.certified_usda_organic)
      formData.append('certified_halal', this.component_data.certified_halal)
      formData.append('certified_kosher', this.component_data.certified_kosher)
      formData.append('certified_gluten_free', this.component_data.certified_gluten_free)
      formData.append('certified_national_sanitation_foundation', this.component_data.certified_national_sanitation_foundation)
      formData.append('certified_us_pharmacopeia', this.component_data.certified_us_pharmacopeia)
      formData.append('certified_non_gmo', this.component_data.certified_non_gmo)
      formData.append('certified_vegan', this.component_data.certified_vegan)
      formData.append('brand_id', this.component_data.brand_id)
      formData.append('units', this.component_data.units)
      this.component_data.doc.remove_files = this.remove_files_buffer
      for (const pair of Object.entries(this.component_data.doc.files)) {
        const key = pair[0]
        const value = pair[1]
        const fileObj = structuredClone(value.file)
        delete value.file
        this.component_data.doc.files[key] = value
        formData.append(key, fileObj)
      }
      formData.append('doc', JSON.stringify(this.component_data.doc))
      formData.append('Component_Names', JSON.stringify(this.component_data.Component_Names))
      try {
        this.loaded = false
        const response = await fetch(fetchRequest, {
          method: 'PUT',
          credentials: 'include',
          body: formData
        })
        if (response.status === 201) {
          const data = await response.json()
          this.flash_messages = data.messages.flash
          const createToast = this.$root.createToast
          this.flash_messages.forEach(function (message) {
            createToast(message)
          })
          this.getComponentData()
          this.loaded = true
          return true
        } else if (response.status === 401) {
          this.$router.push({
            name: 'login'
          })
        } else {
          response.json().then(data => {
            this.flash_messages = data.messages.flash
            const createToast = this.$root.createToast
            this.flash_messages.forEach(function (message) {
              createToast(message)
            })
          })
          this.loaded = true
          return false
        }
      } catch (error) {
        const err = error
        this.loaded = true
        // eslint-disable-next-line
        console.error('There has been a problem with your fetch operation: ', err)
        const errorToast = {
          title: 'Failure to save changes.',
          message: 'Find IT to help fix the issue.',
          variant: 'danger',
          visible: true,
          noCloseButton: false,
          noAutoHide: true,
          autoHideDelay: false,
          appendToast: true,
          solid: true,
          toaster: 'b-toaster-bottom-right'
        }
        const createToast = this.$root.createToast
        createToast(errorToast)
        return false
      }
    }
  },
  created: function () {
    this.getComponentData()
  }
}
</script>

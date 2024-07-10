<template>
  <div v-if="doc.specifications !== undefined">
    <h3 id="Specifications">Specifications<b-button v-if="!edit_specs" v-b-tooltip.hover title="Edit Specifications" v-on:click="editSpecs()" class="btn p-1 ml-2 btn-light" type="button"><b-icon icon="pencil-square" class="d-print-none"></b-icon></b-button></h3>
    <div v-if="!edit_specs">
      <p><strong>Spec Issued: </strong>{{ doc.specifications.date_issued !== undefined && doc.specifications.date_issued !== '' ? new Date(doc.specifications.date_issued).toDateString() : "No Spec" }}</p>
      <p><strong>Spec Revised: </strong>{{ doc.specifications.date_revised !== undefined && doc.specifications.date_revised !== '' ? new Date(doc.specifications.date_revised).toDateString() : "No Spec" }}</p>
      <p><strong>Revision Number: </strong>{{ doc.specifications.revision_number }}</p>
    </div>
    <div v-if="!edit_specs">
      <p v-if="doc.specifications.description_statement.length > 0"><strong>Description</strong><br>{{ doc.specifications.description_statement }}</p>
      <p v-if="doc.specifications.origin.length > 0"><strong>Origin</strong><br>{{ doc.specifications.origin }}</p>
      <p v-if="doc.specifications.identity_statement.length > 0"><strong>Identity Statement</strong><br>{{ doc.specifications.identity_statement }}</p>
      <p v-if="doc.specifications.strength_statement.length > 0"><strong>Strength Statement</strong><br>{{ doc.specifications.strength_statement }}</p>
      <p v-if="doc.specifications.purity_statement.length > 0"><strong>Purity Statement</strong><br>{{ doc.specifications.purity_statement }}</p>
      <p v-if="doc.specifications.parts_used.length > 0"><strong>Parts Used</strong><br>{{ doc.specifications.parts_used }}</p>
    </div>
    <div v-if="edit_specs">
      <b-form-group>
        <label for="description_statement"><strong>Description</strong><br></label>
        <b-form-textarea id="description_statement" v-model="edit_specs_buffer.description_statement" placeholder="description..." rows="3" max-rows="6" v-on:keyup.enter="focus('origin')"></b-form-textarea>
        <label for="origin"><strong>Origin</strong><br></label>
        <b-form-textarea id="origin" v-model="edit_specs_buffer.origin" placeholder="Origin..." rows="3" max-rows="6" v-on:keyup.enter="focus('identity_statement')"></b-form-textarea>
        <label for="identity_statement"><strong>Identity Statement</strong><br></label>
        <b-form-textarea id="identity_statement" v-model="edit_specs_buffer.identity_statement" placeholder="Identity statement..." rows="3" max-rows="6" v-on:keyup.enter="focus('strength_statement')"></b-form-textarea>
        <label for="strength_statement"><strong>Strength Statement</strong><br></label>
        <b-form-textarea id="strength_statement" v-model="edit_specs_buffer.strength_statement" placeholder="Strength statement..." rows="3" max-rows="6" v-on:keyup.enter="focus('purity_statement')"></b-form-textarea>
        <label for="purity_statement"><strong>Purity Statement</strong><br></label>
        <b-form-textarea id="purity_statement" v-model="edit_specs_buffer.purity_statement" placeholder="Purity statement..." rows="3"  max-rows="6" v-on:keyup.enter="focus('description_statement')"></b-form-textarea>
        <label for="parts_used"><strong>Parts Used</strong><br></label>
        <b-form-textarea id="parts_used" v-model="edit_specs_buffer.parts_used" placeholder="Parts used..." rows="1"  max-rows="2"></b-form-textarea>
      </b-form-group>
      <div class="d-flex">
        <b-button v-if="edit_specs" variant="danger" class="m-2" v-on:click="cancelEditSpecs()">Cancel</b-button>
        <b-button type="submit" v-if="edit_specs" variant="success" class="m-2" v-on:click="editSpecs()">Save</b-button>
      </div>
    </div>

    <hr>

    <!-- Generic Specifications -->
    <div v-for="(spec, spec_key, index) in doc.specifications.specs" :key="index" style="break-inside: avoid;">

      <h3 :id="spec_key">{{ spec.test_name }}<b-button v-if="!edit_specs" v-b-tooltip.hover :title="'Edit ' + spec.test_name + ' Specifications'" v-on:click="editSpecs()" class="btn p-1ml-2 btn-light" type="button"><b-icon icon="pencil-square" class="d-print-none"></b-icon></b-button></h3>
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
                <!-- {{ methods }} -->
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
                  <strong>Magnification: </strong><br>
                  <v-select v-model="test.magnification" required label="text" :reduce="mag => mag.value"
                    :options="[{ value: '', text: 'Select Magnification' },{ value: '20X', text: '20X' },{ value: '40X', text: '40X' }]">
                  </v-select>
                  <strong>Method: </strong><br>
                  <v-select v-model="test.method" required label="text" :reduce="methods => methods.value"
                    :options="[{ value: '', text: 'Select Method' }, { value: 'SOP QA 04.02', text: 'SOP QA 04.02' }]">
                  </v-select>
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
                  <strong>Method: </strong><br><v-select v-model="test.method" required label="text" :reduce="mag => mag.value"
                    :options="[{ value: '', text: 'Select Method' }, { value: 'SOP QA 04.02', text: 'SOP QA 04.01' }]"></v-select>
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
                <v-select v-model="test.unit_of_measure" :options="['%','cfu/g','cfu/10g','cfu/25g','ppm','rf']" class="mr-sm-2"
                  placeholder="Select Units" label="text"></v-select>
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
        <b-button v-if="edit_specs" variant="danger" class="m-2" v-on:click="cancelEditSpecs()">Cancel</b-button>
        <b-button type="submit" v-if="edit_specs" variant="success" class="m-2" v-on:click="editSpecs(spec_key)">Save</b-button>
      </div>
      <hr>
    </div>
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
</style>

<script>
import Vue3EasyDataTable from 'vue3-easy-data-table'
import { CustomRequest } from '../../common/CustomRequest.js'
import { cloneDeep } from 'lodash'
import vSelect from 'vue-select'

export default {
  name: 'SpecificationsComponent',
  components: {
    Vue3EasyDataTable,
    vSelect
  },
  props: {
    doc: {
      type: Object,
      required: true
    },
    spectype: {
      type: String,
      required: true
    },
    name: {
      type: String,
      required: true
    },
    id: {
      type: Number,
      required: true
    }
  },
  data: function () {
    return {
      headers: [
        { text: 'Test', value: 'test_name', width: 230 },
        { text: 'Rqd', value: 'required_spec', width: 20 },
        { text: 'Spec', value: 'generated', width: 100 },
        { text: 'Methods', value: 'methods', width: 110 },
        { text: 'Statement', value: 'statement', width: 250 }
      ],
      edit_specs: false,
      edit_specs_buffer: {},
      flash_messages: [],
      req: new CustomRequest(this.$cookies.get('session'))
    }
  },
  methods: {
    focus: function (elmId) {
      document.getElementById(elmId).focus()
    },
    addSpec: function (specKey) {
      const test = this.newTest()
      test.type = this.spectype + '_specifications/' + specKey
      this.edit_specs_buffer.specs[specKey].tests.push(test)
    },
    newCardSpec: function (specKey) {
      const test = this.newTest()
      test.test_name = this.edit_specs_buffer.specs[specKey].test_name
      test.type = this.spectype + '_specifications/' + specKey
      test.required_spec = this.edit_specs_buffer.specs[specKey].required_spec
      this.edit_specs_buffer.specs[specKey].tests.push(test)
    },
    removeTest: function (index, specKey) {
      this.req.deleteFile(this.edit_specs_buffer.specs[specKey].tests[index].file_hash)
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
        file_type: null,
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
    onFileChange: async function (e, test) {
      // Preview File
      const file = e.target.files[0]
      test.url_preview = URL.createObjectURL(file)
      URL.revokeObjectURL(file)

      const customKey = await this.req.addFile(file, 1, test.id_code, test.type)
      test.file_pointer = customKey
    },
    editSpecs: async function (subSpec) {
      if (!this.edit_specs) {
        this.edit_specs_buffer = cloneDeep(this.doc.specifications)
        this.edit_specs = true
        this.$emit('editSpecs', this.edit_specs)
      } else {
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
        if (this.spectype === 'component') {
          this.saveComponentUpdates().then(outcome => {
            if (outcome) {
              this.edit_specs_buffer = []
              this.edit_specs = false
              this.$emit('editSpecs', this.edit_specs)
            }
          })
        } else {
          this.saveProductUpdates().then(outcome => {
            if (outcome) {
              this.edit_specs_buffer = []
              this.edit_specs = false
              this.$emit('editSpecs', this.edit_specs)
            }
          })
        }
      }
    },
    saveComponentUpdates: function () {
      this.$emit('toggleLoaded', false)
      const component = {
        doc: {
          specifications: this.edit_specs_buffer
        },
        component_id: this.id
      }
      this.req.upsertRecord('Components', component)

      return this.req.sendRequest(window.origin).then(resp => {
        const createToast = this.$root.createToast
        resp.messages.flash.forEach(message => {
          createToast(message)
        })

        if (resp.status !== 201) {
          return false
        }
        this.$parent.getProductData()
        this.req = new CustomRequest(this.$cookies.get('session'))
        this.cancelEditSpecs()
        this.$emit('toggleLoaded', true)
        return true
      })
    },
    saveProductUpdates: async function () {
      const product = {
        doc: {
          specifications: this.edit_specs_buffer
        },
        product_id: this.id
      }
      this.req.upsertRecord('Product_Master', product)

      const resp = await this.req.sendRequest(window.origin)
      this.$emit('toggleLoaded', false)
      this.$emit('refreshParent')

      const createToast = this.$root.createToast
      resp.messages.flash.forEach(message => {
        createToast(message)
      })
      // Everything else works
      if (resp.status !== 201) {
        return false
      }
      this.$parent.getComponentData()
      this.req = new CustomRequest(this.$cookies.get('session'))
      this.cancelEditSpecs()
      this.$emit('toggleLoaded', true)
      return true
    },
    cancelEditSpecs: function () {
      this.edit_specs_buffer = []
      this.edit_specs = false
      this.$emit('editSpecs', this.edit_specs)
      this.req = new CustomRequest(this.$cookies.get('session'))
    },
    format_string: function (type) {
      if (type === undefined) {
        return ''
      }
      return type.toLowerCase().split('_').map((s) => s.charAt(0).toUpperCase() + s.substring(1)).join(' ')
    }
  }
}
</script>

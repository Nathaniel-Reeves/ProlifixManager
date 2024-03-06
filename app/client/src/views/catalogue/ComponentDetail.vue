<template>
  <div class="my_component d-flex flex-wrap justify-content-center">
    <div class="card m-2 p-2" v-show="!loaded">
      <div class="card-body">
        <div class="d-flex justify-content-center">
          <div class="spinner-border text-primary" role="status"></div>
        </div>
      </div>
    </div>

    <b-container fluid>
      <b-card class="m-2" v-show="loaded">
        <b-card-body>
          <h2 class="card-title">{{ get_comopnent_primary_name(component_data) }} {{ format_string(component_data.component_type) }}</h2>
          <hr>
          <b-nav pills card-header slot="header" v-b-scrollspy:nav-scroller class="text-nowrap">
            <b-nav-item href="#Aliases" @click="scrollIntoView">Aliases</b-nav-item>
            <b-nav-item href="#Specifications" @click="scrollIntoView" v-if="component_data.doc.specifications !== undefined">Specifications</b-nav-item>
            <div v-for="(spec, spec_key) in component_data.doc.specifications.specs" :key="spec_key">
              <b-nav-item :href="'#'+spec_key" @click="scrollIntoView">{{ spec.test_name }}</b-nav-item>
            </div>
          </b-nav>
        </b-card-body>
      </b-card>

      <b-card class="m-2" v-show="loaded">
        <b-card-body id="nav-scroller" ref="content" style="position:relative; height:60vh; overflow-y:scroll;">

          <!-- Alias Names -->
          <NamesComponent :data="component_data.Component_Names" :save-function="putComponent" naming-type="component"></NamesComponent>
          <hr>

          <!-- Specifications -->
          <div v-if="component_data.doc.specifications !== undefined">
            <h3 id="Specifications">Specifications<b-button v-if="!edit_specs" v-b-tooltip.hover title="Edit Component Specifications" v-on:click="editSpecs()" v-bind:class="['btn','p-1', 'ml-2', 'btn-light']" type="button"><i class="bi bi-pencil-square"></i></b-button></h3>
            <div v-if="!edit_specs">
              <p><strong>Spec Issued: </strong>{{ new Date(component_data.doc.specifications.date_issued).toDateString() }}</p>
              <p><strong>Spec Revised: </strong>{{ new Date(component_data.doc.specifications.date_revised).toDateString() }}</p>
              <p><strong>Revision Number: </strong>{{ component_data.doc.specifications.revision_number }}</p>
            </div>
            <div v-if="!edit_specs">
              <p v-if="component_data.doc.specifications.description_statement.length > 0"><strong>Component Description</strong><br>{{ component_data.doc.specifications.description_statement }}</p>
              <p v-if="component_data.doc.specifications.origin.length > 0"><strong>Origin</strong><br>{{ component_data.doc.specifications.origin }}</p>
              <p v-if="component_data.doc.specifications.identity_statement.length > 0"><strong>Identity Statement</strong><br>{{ component_data.doc.specifications.identity_statement }}</p>
              <p v-if="component_data.doc.specifications.strength_statement.length > 0"><strong>Strength Statement</strong><br>{{ component_data.doc.specifications.strength_statement }}</p>
              <p v-if="component_data.doc.specifications.purity_statement.length > 0"><strong>Purity Statement</strong><br>{{ component_data.doc.specifications.purity_statement }}</p>
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
              </b-form-group>
              <div class="d-flex">
                <b-button v-if="edit_specs" variant="outline-info" class="m-2" v-on:click="cancelEditSpecs()">Cancel</b-button>
                <b-button type="submit" v-if="edit_specs" variant="primary" class="m-2" v-on:click="editSpecs()">Save</b-button>
              </div>
            </div>

            <hr>

            <!-- Generic Specifications -->
            <div v-for="(spec, spec_key, index) in component_data.doc.specifications.specs" :key="index">

              <!-- Spec Header -->
              <h3 :id="spec_key">{{ spec.test_name }}<b-button v-if="!edit_specs" v-b-tooltip.hover :title="'Edit Component ' + spec.test_name + ' Specifications'" v-on:click="editSpecs()" class="btn p-1ml-2 btn-light" type="button"><i class="bi bi-pencil-square"></i></b-button></h3>
              <div v-if="!edit_specs">
                <p><strong>Spec Issued: </strong>{{ new Date(spec.date_issued).toDateString() }}</p>
                <p><strong>Spec Revised: </strong>{{ new Date(spec.date_revised).toDateString() }}</p>
                <p><strong>Revision Number: </strong>{{ spec.revision_number }}</p>
                <p><strong>Accepted Testing Sources: </strong>
                  <b-badge variant="secondary" pill class="ml-2" style="font-size:1em;" v-show="spec.locations.in_house">In House</b-badge>
                  <b-badge variant="secondary" pill class="ml-2" style="font-size:1em;" v-show="spec.locations.third_party_lab">Third Party Lab</b-badge>
                  <b-badge variant="secondary" pill class="ml-2" style="font-size:1em;" v-show="spec.locations.supplier">Supplier</b-badge>
                </p>
                <p><strong>Primary Testing Responsibility: </strong>
                  <b-badge variant="primary" pill class="ml-2" style="font-size:1em;">{{ format_string(spec.locations.primary) }}</b-badge>
                </p>
                <p><strong>Spec Required: </strong><b-badge pill class="ml-2" style="font-size:1em;" v-bind:variant="(spec.required_spec ? 'success' : 'warning')">{{ spec.required_spec ? 'YES' : 'NO' }}</b-badge></p>
                <p v-show="Boolean(spec.statement)"><strong>Statement</strong><br>{{ spec.statement }}</p>
              </div>

              <!-- Edit Spec Header -->
              <div v-if="edit_specs">
                <b-form-group v-slot="{ ariaDescribedby }">
                  <label :for="'spec_accepted_' + spec_key"><strong>Accepted Test Sources: <br></strong></label>
                  <b-form-checkbox :name="'spec_accepted_' + spec_key" v-model="edit_specs_buffer.specs[spec_key].locations.in_house" :aria-describedby="ariaDescribedby">In House</b-form-checkbox>
                  <b-form-checkbox :name="'spec_accepted_' + spec_key" v-model="edit_specs_buffer.specs[spec_key].locations.third_party_lab" :aria-describedby="ariaDescribedby">Third Party Lab</b-form-checkbox>
                  <b-form-checkbox :name="'spec_accepted_' + spec_key" v-model="edit_specs_buffer.specs[spec_key].locations.supplier" :aria-describedby="ariaDescribedby">Supplier</b-form-checkbox>
                </b-form-group>

                <b-form-group v-slot="{ ariaDescribedby }" v-model="edit_specs_buffer.specs[spec_key].locations.primary">
                  <label :for="'spec_responsibility_' + spec_key"><strong>Primary Testing Responsibility: </strong></label>
                  <b-form-radio v-model="edit_specs_buffer.specs[spec_key].locations.primary" :aria-describedby="ariaDescribedby" :name="'spec_responsibility_' + spec_key" value="in_house">In House</b-form-radio>
                  <b-form-radio v-model="edit_specs_buffer.specs[spec_key].locations.primary" :aria-describedby="ariaDescribedby" :name="'spec_responsibility_' + spec_key" value="third_party_lab">Third Party Lab</b-form-radio>
                  <b-form-radio v-model="edit_specs_buffer.specs[spec_key].locations.primary" :aria-describedby="ariaDescribedby" :name="'spec_responsibility_' + spec_key" value="supplier">Supplier</b-form-radio>
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
                <!-- Spec Content -->
                <div v-if="!edit_specs">
                  <!-- Card Type Specs -->
                  <b-card-group deck v-if="useCardType(spec_key)">
                    <div v-for="test, test_key, index in spec.tests" :key="index">
                      <b-card no-body style="max-width: 25rem;" class="my-3 no-shaddow">
                        <b-card-img v-if="(spec_key === 'microscopic' || spec_key === 'organoleptic') && getFile(test.file_pointer)" :src="getFile(test.file_pointer)" top></b-card-img>
                        <b-card-body v-if="spec_key === 'microscopic'">
                          <b-card-title>{{ test.id_code }}</b-card-title>
                          <b-card-text>
                            <p class="mb-2">{{ test.description }}</p>
                            <strong>Magnification: </strong><b-badge variant="secondary" pill class="ml-2" style="font-size:1em;">{{ test.magnification }}</b-badge><br>
                            <strong>Method:  </strong>{{ test.method }}
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
                        <b-card-body v-else>
                          <b-card-title>{{ test.id_code }}</b-card-title>
                        </b-card-body>
                        <b-card-footer>{{ new Date(test.date_revised).toDateString() }}</b-card-footer>
                      </b-card>
                    </div>
                  </b-card-group>

                  <!-- Grid Type Specs -->
                  <div v-else>
                    <Grid :rows="spec.tests" :cols="test_cols"></Grid>
                  </div>
                </div>

                <!-- Edit Spec Content -->
                <div v-if="edit_specs">
                  <!-- Card Type Specs -->
                  <b-card-group deck v-if="useCardType(spec_key)">
                    <div v-for="( test, index ) in edit_specs_buffer.specs[spec_key].tests" :key="index">
                      <b-card no-body style="max-width: 25rem; min-width: 25rem;" class="my-3">
                        <b-card-img :src="test.url_preview || test.url_preview === null ? test.url_preview : getFile(test.file_pointer)" top></b-card-img>
                        <b-card-body v-if="spec_key === 'microscopic'">
                          <b-form-file no-drop required accept="image/png, image/jpeg" v-show="!test.url_preview && !test.file_pointer && test.id_code !== null && test.id_code.length > 3" type="file" class="my-2" @change="onFileChange($event, test)"></b-form-file>
                          <b-form-input v-show="!test.file_pointer" type="text" class="my-1" v-model="test.id_code" placeholder="Lot Number..."></b-form-input>
                          <b-card-title v-show="test.file_pointer && test.id_code !== null && test.id_code.length > 3" class="my-1">{{ test.id_code }}</b-card-title>
                          <strong>Discription: </strong><br><b-form-textarea class="my-1" rows="3" max-rows="3" v-model="test.description" placeholder="Discription..."></b-form-textarea>
                          <strong>Magnification: </strong><br><b-form-select v-model="test.magnification" required :options="[{ value: '', text: 'Select Magnification' },{ value: '20X', text: '20X' },{ value: '40X', text: '40X' }]"></b-form-select>
                          <strong>Method: </strong><br><b-form-select v-model="test.method" required :options="[{ value: '', text: 'Select Method' }, { value: 'SOP QA 04.02', text: 'SOP QA 04.02' }]"></b-form-select>
                        </b-card-body>
                        <b-card-body v-if="spec_key === 'organoleptic'">
                          <b-form-file no-drop required accept="image/png, image/jpeg" v-show="!test.url_preview && !test.file_pointer && test.id_code !== null && test.id_code.length > 3" type="file" class="my-2" @change="onFileChange($event, test)"></b-form-file>
                          <b-form-input v-show="!test.file_pointer" type="text" class="my-1" v-model="test.id_code" placeholder="Lot Number..."></b-form-input>
                          <b-card-title v-show="test.file_pointer && test.id_code !== null && test.id_code.length > 3" class="my-1">{{ test.id_code }}</b-card-title>
                          <strong>Odor: </strong><br><b-form-textarea class="my-1" rows="3" max-rows="3" v-model="test.odor" placeholder="Odor..."></b-form-textarea>
                          <strong>Dissolved Taste: </strong><br><b-form-textarea class="my-1" rows="3" max-rows="3" v-model="test.taste_dissolved" placeholder="Dissolved Taste..."></b-form-textarea>
                          <strong>Dry Taste: </strong><br><b-form-textarea class="my-1" rows="3" max-rows="3" v-model="test.taste_dry" placeholder="Dry Taste..."></b-form-textarea>
                          <strong>Visual: </strong><br><b-form-textarea class="my-1" rows="3" max-rows="3" v-model="test.visual" placeholder="Visual..."></b-form-textarea>
                          <strong>Method: </strong><br><b-form-select v-model="test.method" required :options="[{ value: '', text: 'Select Method' }, { value: 'SOP QA 04.02', text: 'SOP QA 04.01' }]"></b-form-select>
                        </b-card-body>
                        <b-card-footer>
                          <b-button class="my-2" variant="outline-danger" @click="removeTest(index, spec_key)">Remove</b-button>
                        </b-card-footer>
                      </b-card>
                    </div>
                    <b-card v-if="spec_key === 'microscopic'" img-src="../../assets/no_image_placeholder.png" class="my-3" style="max-width: 25rem; min-width: 25rem; cursor: pointer;" v-on:click="newCardSpec(spec_key)">
                      <b-card-title>New Microscopic Image</b-card-title>
                    </b-card>
                    <b-card v-else-if="spec_key === 'organoleptic'" class="my-3" style="max-width: 25rem; min-width: 25rem; cursor: pointer;" v-on:click="newCardSpec(spec_key)">
                      <b-card-title>New Organoleptic Spec</b-card-title>
                    </b-card>
                    <!-- <b-card v-else class="my-3" style="max-width: 25rem; min-width: 25rem; cursor: pointer;" v-on:click="newCardSpec(spec_key)">
                      <b-card-title>New Spec</b-card-title>
                    </b-card> -->
                  </b-card-group>

                  <!-- Grid Type Specs -->
                  <div v-else>
                    <Grid :rows="spec.tests" :cols="test_cols"></Grid>
                  </div>
                </div>
              </div>

              <!-- Spec Action Buttons -->
              <div class="d-flex mt-3" v-if="edit_specs">
                <b-button v-if="edit_specs" variant="outline-info" class="m-2" v-on:click="cancelEditSpecs()">Cancel</b-button>
                <b-button type="submit" v-if="edit_specs" variant="primary" class="m-2" v-on:click="editSpecs(spec_key)">Save</b-button>
              </div>
              <hr>
            </div>
          </div>

          <!-- {{ component_data.doc.specifications }} -->
        </b-card-body>
      </b-card>
    </b-container>
  </div>
</template>

<style scoped>
.bold {
    font-weight: bold;
}
.my_component {
    width: 95%;
}
@media only screen and (max-width: 1024px) {
    .my_component {
        width: 98%;
    }
}
</style>

<script>
import NamesComponent from './NamesComponent.vue'
import Grid from 'gridjs-vue'
import { html } from 'gridjs'

export default {
  name: 'ComponentDetail',
  components: {
    NamesComponent,
    Grid
  },
  data: function () {
    return {
      id: this.$route.params.id,
      component_data: {},
      search_query: '',
      loaded: false,
      test_cols: [
        {
          id: 'test_name',
          name: 'Test'
        },
        {
          id: 'required_spec',
          name: 'Rqd',
          formatter: (cell) => (cell ? html('<span class="badge ml-2 badge-success badge-pill" style="font-size: 1em;">Yes</span>') : html('<span class="badge ml-2 badge-warning badge-pill" style="font-size: 1em;">No</span>')),
          width: '1em'
        },
        {
          id: 'greater_than',
          hidden: true
        },
        {
          id: 'less_than',
          hidden: true
        },
        {
          id: 'count',
          name: 'Count',
          hidden: true
        },
        {
          id: 'unit_of_measure',
          name: 'UoM',
          hidden: true
        },
        {
          name: 'Spec',
          formatter: (_, row) => (
            (row.cells[2].data ? '>' : '') +
            (row.cells[3].data ? '<' : '') +
            row.cells[4].data +
            ' ' +
            row.cells[5].data
          ),
          width: '20%'
        },
        {
          id: 'methods',
          name: 'Methods',
          formatter: (cell) => {
            let d = ''
            cell.forEach((method) => {
              d += ' ' + method + '<br>'
            })
            return html(d)
          }
        },
        {
          id: 'statement',
          name: 'Statement',
          width: '100%'
        }
      ],
      edit_names: false,
      edit_names_buffer: [],
      edit_specs: false,
      edit_specs_buffer: {},
      upload_files_buffer: {},
      flash_messages: [],
      file_index: 1
    }
  },
  methods: {
    newCardSpec: function (specKey) {
      const test = this.newTest()
      test.test_name = this.edit_specs_buffer.specs[specKey].test_name
      test.type = 'component_specifications/' + specKey
      test.required_spec = this.edit_specs_buffer.specs[specKey].required_spec
      this.edit_specs_buffer.specs[specKey].tests.push(test)
    },
    removeTest: function (index, specKey) {
      for (const pair in this.edit_files_buffer) {
        if (this.edit_specs_buffer.specs[specKey].tests[index].file_pointer === pair[0]) {
          this.edit_files_buffer.splice(pair[0], 1)
        }
      }
      this.edit_specs_buffer.specs[specKey].tests.splice(index, 1)
    },
    newTest: function () {
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
        rf_value: 0,
        mesh_size: 0,
        percent: 0,
        count: 0,
        amount_per_serving: 0,
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
        date_issued: new Date().toISOString(),
        date_revised: new Date().toISOString(),
        url_preview: null
      }
    },
    getFile: function (filename) {
      if (filename) {
        const fetchRequest = window.origin + '/api/v1/uploads/' + filename
        return fetchRequest
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
        'hptlc'
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
        this.edit_specs_buffer.revision_number++
        this.edit_specs_buffer.date_revised = new Date().toISOString() // Today
        if (subSpec !== undefined) {
          this.edit_specs_buffer.specs[subSpec].revision_number++
          this.edit_specs_buffer.specs[subSpec].date_revised = new Date().toISOString() // Today
        }
        this.component_data.doc.specifications = structuredClone(this.edit_specs_buffer) // Deep Copy
        this.component_data.doc.files = structuredClone(this.upload_files_buffer)
        this.putComponent().then(outcome => {
          if (outcome === true) {
            this.edit_specs_buffer = []
            this.upload_files_buffer = {}
            this.edit_specs = false
          } else {
            this.component_data.doc.specifications = original
          }
        })
      }
    },
    cancelEditSpecs: function () {
      this.edit_specs_buffer = []
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
    get_component_brand_name: function (component) {
      if (component.Organization_Names !== undefined && component.Organization_Names.length > 0) {
        for (let i = 0; i < component.Organization_Names.length; i++) {
          if (component.Organization_Names[i].primary_name) {
            return component.Organization_Names[i].organization_name
          }
        }
      }
      return ''
    },
    getComponentData: function () {
      const fetchRequest = window.origin + '/api/v1/catalogue/components?component-id=' + this.id + '&populate=product_materials&populate=purchase_order_detail&populate=label_formula_master&populate=ingredient_formula_master&populate=item_id&populate=inventory&populate=brand&doc=true'
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
            console.log(this.component_data)
            this.loaded = true
          })
        } else if (response.status === 401) {
          this.$router.push({
            name: 'login'
          })
        } else {
          console.log('Looks like there was a problem. Status Code:' + response.status)
          console.log(response)
        }
      })
    },
    putComponent: async function () {
      const fetchRequest = window.origin + '/api/v1/catalogue/components'
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
        console.log(this.component_data)
        const response = await fetch(fetchRequest, {
          method: 'PUT',
          credentials: 'include',
          body: formData
        })
        if (response.status === 201) {
          const data = await response.json()
          this.flash_messages = data.messages.flash
          const createToast = this.$parent.createToast
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
            const createToast = this.$parent.createToast
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
        const createToast = this.$parent.createToast
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

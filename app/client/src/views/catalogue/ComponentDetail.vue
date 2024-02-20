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
            <b-nav-item href="#Organoleptic" @click="scrollIntoView" v-if="component_data.doc.specifications !== undefined && component_data.doc.specifications.organoleptic !== undefined">Organoleptic</b-nav-item>
            <b-nav-item href="#Sterio_Microscopic" @click="scrollIntoView" v-if="component_data.doc.specifications !== undefined && component_data.doc.specifications.microscopic !== undefined">Sterio Microscopic</b-nav-item>
            <b-nav-item href="#Microbiological" @click="scrollIntoView" v-if="component_data.doc.specifications !== undefined && component_data.doc.specifications.microbiological !== undefined">Microbiological</b-nav-item>
            <b-nav-item href="#Gluten" @click="scrollIntoView" v-if="component_data.doc.specifications !== undefined && component_data.doc.specifications.gluten !== undefined">Gluten</b-nav-item>
            <b-nav-item href="#FTIR" @click="scrollIntoView" v-if="component_data.doc.specifications !== undefined && component_data.doc.specifications.ftir !== undefined">FTIR</b-nav-item>
            <b-nav-item href="#HPLC" @click="scrollIntoView" v-if="component_data.doc.specifications !== undefined && component_data.doc.specifications.hplc !== undefined">HPLC</b-nav-item>
            <b-nav-item href="#HPTLC" @click="scrollIntoView" v-if="component_data.doc.specifications !== undefined && component_data.doc.specifications.hptlc !== undefined">HPTLC</b-nav-item>
            <b-nav-item href="#Nutritional_Facts" @click="scrollIntoView" v-if="component_data.doc.specifications !== undefined && component_data.doc.specifications.nutritional_facts !== undefined">Nutritional Facts</b-nav-item>
            <b-nav-item href="#Pesticides" @click="scrollIntoView" v-if="component_data.doc.specifications !== undefined && component_data.doc.specifications.pesticides !== undefined">Pesticides</b-nav-item>
            <b-nav-item href="#Herbicides" @click="scrollIntoView" v-if="component_data.doc.specifications !== undefined && component_data.doc.specifications.herbicides !== undefined">Herbicides</b-nav-item>
            <b-nav-item href="#Insecticides" @click="scrollIntoView" v-if="component_data.doc.specifications !== undefined && component_data.doc.specifications.insecticides !== undefined">Insecticides</b-nav-item>
            <b-nav-item href="#Organochlorines" @click="scrollIntoView" v-if="component_data.doc.specifications !== undefined && component_data.doc.specifications.organochlorines !== undefined">Organochlorines</b-nav-item>
            <b-nav-item href="#Foreign_Matter" @click="scrollIntoView" v-if="component_data.doc.specifications !== undefined && component_data.doc.specifications.foreign_matter !== undefined">Foreign Matter</b-nav-item>
            <b-nav-item href="#Residual_Solvents" @click="scrollIntoView" v-if="component_data.doc.specifications !== undefined && component_data.doc.specifications.residual_solvents !== undefined">Residual Solvents</b-nav-item>
          </b-nav>
        </b-card-body>
      </b-card>

      <b-card class="m-2" v-show="loaded">
        <b-card-body id="nav-scroller" ref="content" style="position:relative; height:60vh; overflow-y:scroll;">

          <!-- Alias Names-->
          <div>
            <h3 id="Aliases">Aliases<b-button v-show="!edit_names" v-b-tooltip.hover title="Edit Component Names" v-on:click="editNames()" v-bind:class="['btn','p-1', 'ml-2', 'btn-light']" type="button"><i class="bi bi-pencil-square"></i></b-button></h3>
            <div v-for="Component_Name in component_data.Component_Names" :key="Component_Name.name_id">
            <p v-show="!edit_names" v-bind:class="{ bold: Component_Name.primary_name, italic: Component_Name.botanical_name}">
              {{ Component_Name.component_name }}{{ Component_Name.primary_name?" | Primary":""}}{{ Component_Name.botanical_name ? " | Botanical" : "" }}
            </p>
            </div>
            <div v-for="Component_Name in edit_names_buffer" :key="'edit' + Component_Name.name_id">
            <b-form inline v-show="edit_names" class="m-2">
              <label class="sr-only" for="inline-form-input-name">Name</label>
              <b-form-input
                id="inline-form-input-name"
                class="mb-2 mr-sm-2 mb-sm-0"
                v-model="Component_Name.component_name"
                ></b-form-input>
              <div v-on:click="radioNames(Component_Name.name_id, 'primary')">
                <b-form-checkbox button button-variant="light" name="Primary Name" class="mb-2 mr-sm-2 mb-sm-0" v-model="Component_Name.primary_name">Primary Name</b-form-checkbox>
              </div>
              <div v-on:click="radioNames(Component_Name.name_id, 'botanical')" v-show="component_data.component_type === 'powder'">
                <b-form-checkbox button button-variant="light" name="Botanical Name" class="mb-2 mr-sm-2 mb-sm-0" v-model="Component_Name.botanical_name">Botanical Name</b-form-checkbox>
              </div>
              <div>
                <b-button variant="outline-danger" class="mb-2 mr-sm-2 mb-sm-0" v-show="!Component_Name.primary_name" v-on:click="deleteName(Component_Name.name_id)">Delete</b-button>
              </div>
            </b-form>
            </div>
            <div class="d-flex">
            <div v-show="edit_names">
              <b-button variant="outline-info" class="m-2" v-on:click="addName()">New Name</b-button>
              <b-button variant="outline-info" class="m-2" v-on:click="cancelEditNames()">Cancel</b-button>
              <b-button v-show="edit_names_buffer.length > 0" variant="primary" class="m-2" v-on:click="editNames()">Save</b-button>
            </div>
            </div>
          </div>

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
                <b-button v-if="edit_specs" variant="primary" class="m-2" v-on:click="editSpecs()">Save</b-button>
              </div>
            </div>
            <!-- Specifications Organoleptic -->
            <div v-if="component_data.doc.specifications.organoleptic !== undefined">
              <h3 id="Organoleptic">Organoleptic<b-button v-if="!edit_specs" v-b-tooltip.hover title="Edit Component Organoleptic Specifications" v-on:click="editSpecs()" v-bind:class="['btn', 'p-1', 'ml-2', 'btn-light']" type="button"><i class="bi bi-pencil-square"></i></b-button></h3>
              <div v-if="!edit_specs">
                <p><strong>Spec Issued: </strong>{{ new Date(component_data.doc.specifications.organoleptic.date_issued).toDateString() }}</p>
                <p><strong>Spec Revised: </strong>{{ new Date(component_data.doc.specifications.organoleptic.date_revised).toDateString() }}</p>
                <p><strong>Revision Number: </strong>{{ component_data.doc.specifications.organoleptic.revision_number }}</p>
              </div>
              <div v-if="!edit_specs">
                <p><strong>Spec Required: </strong><b-badge pill v-bind:variant="(component_data.doc.specifications.organoleptic.required_spec ? 'success' : 'warning')">{{ component_data.doc.specifications.organoleptic.required_spec ? 'YES' : 'NO' }}</b-badge></p>
                <p><strong>Primary Testing Responsibility: </strong>{{ format_string(component_data.doc.specifications.organoleptic.locations.primary) }}</p>
              </div>
              <div v-if="edit_specs">
                <b-form-group>
                  <div class="d-flex">
                    <label for="Spec Required Organoleptic"><strong>Spec Required: </strong></label>
                    <b-form-checkbox class="ml-2" v-model="edit_specs_buffer.organoleptic.required_spec" name="Spec Required Organoleptic" switch>
                        <b-badge pill v-bind:variant="(edit_specs_buffer.organoleptic.required_spec ? 'success' : 'warning')">{{ edit_specs_buffer.organoleptic.required_spec ? 'YES' : 'NO' }}</b-badge>
                    </b-form-checkbox>
                  </div>
                </b-form-group>
                <div class="d-flex">
                  <b-button v-if="edit_specs" variant="outline-info" class="m-2" v-on:click="cancelEditSpecs()">Cancel</b-button>
                  <b-button v-if="edit_specs" variant="primary" class="m-2" v-on:click="editSpecs('organoleptic')">Save</b-button>
                </div>
              </div>
            </div>
            <!-- Specifications Sterio_Microscopic -->
            <div v-if="component_data.doc.specifications.microscopic !== undefined">
              <h3 id="Sterio_Microscopic">Sterio Microscopic<b-button v-if="!edit_specs" v-b-tooltip.hover title="Edit Component Microscopic Specifications" v-on:click="editSpecs()" v-bind:class="['btn', 'p-1', 'ml-2', 'btn-light']" type="button"><i class="bi bi-pencil-square"></i></b-button></h3>
              <div v-if="!edit_specs">
                <p><strong>Spec Issued: </strong>{{ new Date(component_data.doc.specifications.microscopic.date_issued).toDateString() }}</p>
                <p><strong>Spec Revised: </strong>{{ new Date(component_data.doc.specifications.microscopic.date_revised).toDateString() }}</p>
                <p><strong>Revision Number: </strong>{{ component_data.doc.specifications.microscopic.revision_number }}</p>
              </div>
              <div v-if="!edit_specs">
                <p><strong>Spec Required: </strong><b-badge pill v-bind:variant="(component_data.doc.specifications.microscopic.required_spec ? 'success' : 'warning')">{{ component_data.doc.specifications.microscopic.required_spec ? 'YES' : 'NO' }}</b-badge></p>
                <p><strong>Primary Testing Responsibility: </strong>{{ format_string(component_data.doc.specifications.microscopic.locations.primary) }}</p>
                <b-img :src="getFile(component_data.doc.specifications.microscopic.tests.sterio_microscope.file_pointer)" fluid alt="Responsive image"></b-img>
              </div>
              <div v-if="edit_specs">
                <b-form-group>
                  <div class="d-flex">
                    <label for="Spec Required Microscopic"><strong>Spec Required: </strong></label>
                    <b-form-checkbox class="ml-2" v-model="edit_specs_buffer.microscopic.required_spec" name="Spec Required Microscopic" switch>
                        <b-badge pill v-bind:variant="(edit_specs_buffer.microscopic.required_spec ? 'success' : 'warning')">{{ edit_specs_buffer.microscopic.required_spec ? 'YES' : 'NO' }}</b-badge>
                    </b-form-checkbox>
                  </div>
                </b-form-group>
                <div class="d-flex">
                  <b-button v-if="edit_specs" variant="outline-info" class="m-2" v-on:click="cancelEditSpecs()">Cancel</b-button>
                  <b-button v-if="edit_specs" variant="primary" class="m-2" v-on:click="editSpecs('microscopic')">Save</b-button>
                </div>
              </div>
            </div>
          </div>

          <!-- {{ component_data.doc.specifications }} -->
        </b-card-body>
      </b-card>
    </b-container>
  </div>
</template>

<style scoped>
.my_component {
    width: 75%;
}
@media only screen and (max-width: 1024px) {
    .my_component {
        width: 98%;
    }
}
.bold {
    font-weight: bold;
}
.italic {
    font-style: italic;
}
.normal {
    font-weight: normal;
}
</style>

<script>
export default {
  name: 'ComponentDetail',
  data: function () {
    return {
      id: this.$route.params.id,
      component_data: {},
      search_query: '',
      loaded: false,
      edit_names: false,
      edit_names_buffer: [],
      edit_specs: false,
      edit_specs_buffer: {},
      edit_specs_organoleptic: false,
      edit_specs_organoleptic_buffer: {},
      flash_messages: []
    }
  },
  methods: {
    editSpecs: function (subSpec) {
      const original = structuredClone(this.component_data.doc.specifications) // Deep Copy
      if (!this.edit_specs) {
        this.edit_specs_buffer = structuredClone(this.component_data.doc.specifications) // Deep Copy
        this.edit_specs = true
      } else {
        this.component_data.doc.specifications = {}
        this.edit_specs_buffer.revision_number++
        this.edit_specs_buffer.date_revised = new Date().toISOString()
        if (subSpec !== undefined) {
          this.edit_specs_buffer[subSpec].revision_number++
          this.edit_specs_buffer[subSpec].date_revised = new Date().toISOString()
        }
        this.component_data.doc.specifications = structuredClone(this.edit_specs_buffer) // Deep Copy
        this.putComponent().then(outcome => {
          if (outcome === true) {
            this.edit_specs_buffer = []
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
    radioNames: function (id, flag) {
      for (let i = 0; i < this.edit_names_buffer.length; i++) {
        if (this.edit_names_buffer[i].name_id === id) {
          continue
        } else {
          if (flag === 'botanical') {
            this.edit_names_buffer[i].botanical_name = false
          } else if (flag === 'primary') {
            this.edit_names_buffer[i].primary_name = false
          } else {
            continue
          }
        }
      }
    },
    editNames: function () {
      const original = structuredClone(this.component_data.Component_Names) // Deep Copy
      if (!this.edit_names) {
        this.edit_names_buffer = structuredClone(this.component_data.Component_Names) // Deep Copy
        this.edit_names = true
      } else {
        this.component_data.Component_Names = []
        this.component_data.Component_Names = structuredClone(this.edit_names_buffer) // Deep Copy
        this.putComponent().then(outcome => {
          if (outcome === true) {
            this.edit_names_buffer = []
            this.edit_names = false
          } else {
            this.component_data.Component_Names = original
          }
        })
      }
    },
    cancelEditNames: function () {
      this.edit_names_buffer = []
      this.edit_names = false
    },
    addName: function () {
      const newName = {
        name_id: (Math.random() + 1).toString(36).substring(7),
        component_id: this.component_data.component_id,
        component_name: '',
        primary_name: false,
        botanical_name: false
      }
      this.edit_names_buffer.push(newName)
    },
    deleteName: function (id) {
      for (let i = 0; i < this.edit_names_buffer.length; i++) {
        if (this.edit_names_buffer[i].name_id === id) {
          this.edit_names_buffer.splice(i, 1)
        }
      }
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
    putComponent: function () {
      const fetchRequest = window.origin + '/api/v1/catalogue/components'
      console.log(
        'PUT ' + fetchRequest
      )
      const formData = new FormData()
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
      formData.append('doc', JSON.stringify(this.component_data.doc))
      formData.append('Component_Names', JSON.stringify(this.component_data.Component_Names))
      try {
        this.loaded = false
        return fetch(fetchRequest, {
          method: 'PUT',
          credentials: 'include',
          body: formData
        }).then(response => {
          if (response.status === 201) {
            response.json().then(data => {
              this.flash_messages = data.messages.flash
              const createToast = this.$parent.createToast
              this.flash_messages.forEach(function (message) {
                createToast(message)
              })
            })
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
        })
      } catch (error) {
        this.loaded = true
        console.error('There has been a problem with your fetch operation: ', error)
        return false
      }
    },
    getFile: function (filename) {
      const fetchRequest = window.origin + '/api/v1/uploads/' + filename
      console.log(
        'GET ' + fetchRequest
      )
      return fetchRequest
    }
  },
  created: function () {
    this.getComponentData()
  }
}
</script>

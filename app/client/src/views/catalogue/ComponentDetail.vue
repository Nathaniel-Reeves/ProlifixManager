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
          <SpecificationsComponent :data="component_data.doc" :spectype="'component'" :name="get_comopnent_primary_name(component_data)" @update-spec-buffer="update_spec_buffer" @update-file-buffer="update_file_buffer" @update-remove-file-buffer="update_remove_file_buffer" @save-specs="save_specs"></SpecificationsComponent>

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
import SpecificationsComponent from './SpecificationsComponent.vue'

export default {
  name: 'ComponentDetail',
  components: {
    NamesComponent,
    CertBadge,
    SpecificationsComponent
  },
  data: function () {
    return {
      id: this.$route.params.id,
      component_data: {},
      loaded: false,
      edit_names: false,
      edit_names_buffer: [],
      edit_specs: false,
      edit_specs_buffer: {},
      upload_files_buffer: {},
      remove_files_buffer: [],
      flash_messages: []
    }
  },
  methods: {
    update_spec_buffer: function (data) {
      console.log('UPDATE_SPECS', data)
      this.edit_specs_buffer = data
    },
    update_file_buffer: function (data) {
      this.upload_files_buffer = data
    },
    update_remove_file_buffer: function (data) {
      this.remove_files_buffer = data
    },
    save_specs: function () {
      const original = structuredClone(this.component_data.doc.specifications) // Deep Copy
      this.component_data.doc.specifications = structuredClone(this.edit_specs_buffer) // Deep Copy
      this.component_data.doc.files = structuredClone(this.upload_files_buffer) // Deep Copy
      this.putComponent().then(outcome => {
        if (outcome !== true) {
          this.component_data.doc.specifications = original
        }
      })
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

<template>
  <b-card no-body style="width: 25rem;" class="my-3 no-shaddow d-print-block">
      <b-card-img :src="url_preview || url_preview === null ? url_preview : getFile(file_pointer)" top></b-card-img>
        <b-card-body>
          <b-form-file
            no-drop
            required
            accept="image/png, image/jpeg"
            type="file"
            class="my-2"
            @change="onFileChange($event)"
            v-model="file"
          >
        </b-form-file>
        <b-button variant="outline-primary" @click="saveFile()">Save</b-button>
        {{ base64 }}
      </b-card-body>
  </b-card>
</template>

<script>
export default {
  name: 'TestAPI',
  data: function () {
    return {
      file_pointer: '',
      file_index: 0,
      upload_files_buffer: {},
      url_preview: null,
      file: null,
      base64: null
    }
  },
  methods: {
    getFile: function (filename) {
      if (filename) {
        const url = window.origin + '/api/v1/uploads/' + filename
        return url
      } else {
        return ''
      }
    },
    saveFile: function () {
      const request = {
        user_session_key: this.$cookies.get('session'),
        payload: {
          upsert: {
            Components: [
              {
                component_id: 431,
                component_type: 'powder',
                certified_fda: true,
                certified_gmp: true,
                certified_made_with_organic: true,
                certified_wildcrafted: true,
                certified_usda_organic: true,
                certified_halal: true,
                certified_kosher: true,
                certified_gluten_free: true,
                certified_national_sanitation_foundation: true,
                certified_us_pharmacopeia: true,
                certified_non_gmo: true,
                certified_vegan: true,
                units: 'kilograms',
                doc: {
                  specifications: {
                    date_issued: '',
                    date_revised: '',
                    file_pointer: '',
                    revision_number: 0,
                    id_code: '',
                    description_statement: '',
                    identity_statement: '',
                    purity_statement: 'This ingredient is verified for purity via the supplier\'s Certificate of Analysis and through microscopy observation (checking for contaminating particles.) We verify this supplier through a reviewed questionnaire and verify the supplier\'s certificate of analysis on a random/skip lot basis.',
                    strength_statement: '',
                    origin: '',
                    parts_used: '',
                    specs: {
                      example_cofas: {
                        date_issued: '',
                        date_revised: '',
                        file_pointer: '',
                        id_code: '',
                        locations: {
                          in_house: true,
                          primary: 'in_house',
                          supplier: true,
                          third_party_lab: false
                        },
                        required_spec: true,
                        revision_number: 0,
                        test_name: 'Reference CofA\'s',
                        tests: [
                          {
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
                            file_pointer: 'file_0',
                            file_preview_pointer: null,
                            date_issued: new Date().toISOString(),
                            date_revised: new Date().toISOString(),
                            url_preview: null
                          }
                        ]
                      },
                      microscopic: {
                        date_issued: '',
                        date_revised: '',
                        file_pointer: '',
                        locations: {
                          in_house: true,
                          primary: 'in_house',
                          supplier: false,
                          third_party_lab: false
                        },
                        required_spec: true,
                        revision_number: 0,
                        id_code: '',
                        statement: '',
                        test_name: 'Microscopic',
                        tests: [
                          {
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
                            file_pointer: 'file_0',
                            file_preview_pointer: null,
                            date_issued: new Date().toISOString(),
                            date_revised: new Date().toISOString(),
                            url_preview: null
                          }
                        ]
                      }
                    }
                  }
                }
              }
            ]
            // Product_Master: [
            //   {
            //     product_id: 't-46724',
            //     organization_id: 1,
            //     product_name: 'Test Product',
            //     current_product: true,
            //     default_formula_version: 1,
            //     num_formula_versions: 1,
            //     default_manufacturing_version: 3,
            //     num_manufacturing_versions: 3,
            //     exp_unit: 'Years',
            //     exp_type: 'Best_By',
            //     exp_use_oldest_ingredient: false,
            //     certified_fda: false,
            //     certified_gmp: false,
            //     certified_made_with_organic: false,
            //     certified_wildcrafted: false,
            //     certified_usda_organic: false,
            //     certified_halal: false,
            //     certified_kosher: false,
            //     certified_gluten_free: false,
            //     certified_national_sanitation_foundation: false,
            //     certified_us_pharmacopeia: false,
            //     certified_non_gmo: false,
            //     certified_vegan: false,
            //     doc: {}
            //   }
            // ]
          },
          delete: {
            Product_Master: [
              {
                product_id: 127
              },
              {
                product_id: 128
              }
            ]
          }
        },
        upsert_file_data: {},
        delete_file_data: []
      }
      this.saveFileToBuffer()
      request.upsert_file_data = this.upload_files_buffer
      const fetchRequest = window.origin + '/api/v1/submit'
      console.log(
        'PUT ' + fetchRequest
      )
      console.log(request)
      fetch(fetchRequest, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(request)
      })
        .then(response => response.json())
        .then(data => {
          console.log('Success:', data)
          this.flash_messages = data.messages.flash
          const createToast = this.$root.createToast
          this.flash_messages.forEach(function (message) {
            createToast(message)
          })
        })
        .catch((error) => {
          console.error('Error:', error)
        })
    },
    onFileChange: function (e) {
      // Preview File
      const file = e.target.files[0]
      this.url_preview = URL.createObjectURL(file)
      URL.revokeObjectURL(file)
      this.file = file
    },
    saveFileToBuffer: function () {
      const newFile = {
        filename: this.file.name,
        type: this.file.type,
        page: 1,
        size: this.file.size,
        id_code: 'code',
        data_uri: this.base64
      }
      const customKey = 'file_' + this.file_index
      const obj = {}
      obj[customKey] = newFile
      Object.assign(this.upload_files_buffer, obj)
      this.file_index += 1
    },
    createBase64Image: function (FileObject) {
      const reader = new FileReader()
      reader.onload = (event) => {
        this.base64 = event.target.result
      }
      reader.readAsDataURL(FileObject)
    }
  },
  watch: {
    file: function (newVal, oldVal) {
      if (newVal) {
        this.createBase64Image(newVal)
      } else {
        this.base64 = null
      }
    }
  }
}
</script>

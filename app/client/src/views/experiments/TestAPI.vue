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
import CustomRequest from '../common/CustomRequest.js'

export default {
  name: 'TestAPI',
  data: function () {
    return {
      file_pointer: '',
      file_index: 0,
      upload_files_buffer: {},
      url_preview: null,
      file: null,
      base64: null,
      req: new CustomRequest(this.$cookies.get('session'))
    }
  },
  methods: {
    getFile: function (filename) {
      if (filename) {
        const url = this.$root.getOrigin() + '/api/v1/uploads/' + filename
        return url
      } else {
        return ''
      }
    },
    saveFile: async function () {
      const component = {
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
                tests: []
              }
            }
          }
        }
      }

      await this.req.addFile(this.file, 1, 'code')
      this.req.upsertRecord('Components', component)

      const resp = await this.req.sendRequest(this.$root.getOrigin())
      this.req = new CustomRequest(this.$cookies.get('session'))
      const createToast = this.$root.createToast
      resp.messages.flash.forEach(function (message) {
        createToast(message)
      })
    },
    onFileChange: function (e) {
      // Preview File
      const file = e.target.files[0]
      this.url_preview = URL.createObjectURL(file)
      URL.revokeObjectURL(file)
      this.file = file
    }
  }
}
</script>

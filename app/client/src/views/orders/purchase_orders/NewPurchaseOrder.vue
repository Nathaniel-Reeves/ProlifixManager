<template>
 <div class="my_component d-flex justify-content-center">
    <div v-if="!loaded" class="d-flex justify-content-center">
      <div class="card my-2" style="box-shadow: 0 20px 40px rgba(0,0,0,.2); max-width:fit-content;">
        <div class="card-body">
          <div class="d-flex justify-content-center">
            <div class="spinner-border text-primary" role="status"></div>
          </div>
        </div>
      </div>
    </div>
    <div class="card my-2 select_org_card" v-else-if="!supplier_selected">
      <div class="card-body">
        <h2 class="card-title flex-grow-1">New Purchase</h2>
        <b-form>
          <b-container class="my-3" fluid>
            <b-row class="mb-3">
              <b-col>
                <b-button @click="client_purchase = false" :variant="client_purchase ? 'outline-info' : 'info'" block v-b-tooltip.hover title="Direct purchase from Prolifix Nutrition LLC.">Prolifix Purchase</b-button>
              </b-col>
              <b-col >
                <b-button @click="client_purchase = true;getClients()" :variant="client_purchase ? 'info' : 'outline-info'" block v-b-tooltip.hover title="A client has made a purchase and is dropshipping the order to Prolifix Nutrition LLC.">Client Purchase</b-button>
              </b-col>
            </b-row>
            <b-row class="my-3" v-if="client_purchase">
              <b-col md="2">
                <span>Client: </span>
              </b-col>
              <b-col class="d-flex flex-row flex-nowrap">
                <ChooseOrg :organizations="clients" :selected="selected_client_buffer" @org="(o) => selected_client_buffer = o" :org-req="true" :disabled-prop="client_selected" :initial="false"></ChooseOrg>
              </b-col>
            </b-row>
            <b-row class="my-3">
              <b-col md="2">
                <span>Supplier: </span>
              </b-col>
              <b-col class="d-flex flex-row flex-nowrap">
                <ChooseOrg :organizations="suppliers" :selected="selected_supplier_buffer" @org="(o) => selected_supplier_buffer = o" :org-req="true" :disabled-prop="supplier_selected" :initial="false"></ChooseOrg>
              </b-col>
            </b-row>
          </b-container>
          <div class="d-flex justify-content-center">
            <p>Select the supplier before moving forward with order details.</p>
          </div>
          <div class="m-3">
            <b-button block variant="outline-success" @click="setSupplier();setClient()" :disabled="!selected_supplier_buffer?.organization_id">Continue</b-button>
          </div>
        </b-form>
      </div>
    </div>
    <div class="card my-2" v-else style="width:100%;">
      <div
        v-b-visible="handleVisible"
        class="position-fixed d-block d-lg-none"
        style="z-index: 20000; height: 1px;"
      ></div>
      <div class="card-body">
        <h2 v-if="!client_purchase">
          New <router-link class="text-info" :to="'/organizations/'+selected_supplier.organization_id" target="_blank">{{ selected_supplier.organization_primary_name }}</router-link> Order
        </h2>
        <h2 v-else>
          New <router-link class="text-info" :to="'/organizations/'+selected_client.organization_id" target="_blank">{{ selected_client.organization_primary_name }}</router-link> Dropshipping From <router-link class="text-info" :to="'/organizations/'+selected_supplier.organization_id" target="_blank">{{ selected_supplier.organization_primary_name }}</router-link>
        </h2>
        <b-form>
          <div>
            <div class="d-flex justify-content-center" v-if="components.length === 0">
              <div class="spinner-border text-primary" role="status"></div>
            </div>
            <div v-else>
              <b-container class="my-3" fluid>
                <b-row class="mb-2">
                  <b-col md="1">
                    <span>Order Number: </span>
                  </b-col>
                  <b-col md="4">
                    <div class="input-group">
                      <b-form-input v-model="order_buffer.supplier_so"
                        aria-describedby="supplier_so-live-feedback"
                        :class="[(order_buffer.supplier_so.length > 0 ? '' : 'is-invalid')]"
                      ></b-form-input>
                      <div id="supplier_so-live-feedback" class="invalid-feedback">This is a required field.</div>
                    </div>
                  </b-col>
                  <b-col md="1">
                    <span>Tracking: </span>
                  </b-col>
                  <b-col md="4">
                    <div class="input-group">
                      <b-form-input v-model="order_buffer.tracking"
                      ></b-form-input>
                    </div>
                  </b-col>
                </b-row>
                <b-row class="mb-2">
                  <b-col md="1">
                    <span>Date Ordered: </span>
                  </b-col>
                  <b-col md="4">
                    <b-form-datepicker
                      id="order_date"
                      v-model="order_buffer.order_date"
                      :max="new Date()"
                      :class="[(order_buffer.order_date !== null ? '' : 'is-invalid')]"
                    ></b-form-datepicker>
                    <div id="order_date-live-feedback" class="invalid-feedback">This is a required field.</div>
                  </b-col>
                  <b-col md="1">
                    <span>ETA: </span>
                  </b-col>
                  <b-col md="4">
                    <b-form-datepicker
                      id="eta"
                      v-model="order_buffer.eta_date"
                      :min="order_buffer.order_date"
                    ></b-form-datepicker>
                  </b-col>
                </b-row>
              </b-container>
              <b-table stacked="sm" :items="selected_components" :fields="[
                { key: 'action', label: '', thStyle: { width: '2%' } },
                { key: 'component_name', label: 'Component', thStyle: { width: '20%' } },
                { key: 'cert', label: '', thStyle: { width: '20%' } },
                { key: 'order_units', label: 'Units', thStyle: { width: '8%' } },
                { key: 'price_per', label: 'Price', thStyle: { width: '18%' } },
                { key: 'order_qty', label: 'Qty', thStyle: { width: '12%' } },
                { key: 'details', label: 'Details', thStyle: { width: '20%' } }
              ]" class="px-2">
                <template #cell(action)="row">
                  <b-button size="sm" @click="removeComponent(row.index)" variant="outline-danger" v-b-tooltip.hover title="Remove Component">
                    <b-icon icon="trash"></b-icon>
                  </b-button>
                </template>
                <template #cell(component_name)="row">
                  <ChooseComponent :components="components" :selected="row.item" @comp="(c) => row.item = updateComponent(row.item, c, row.index)" :disable-after-entry="false" :comp-req="true" :no-certs="true"></ChooseComponent>
                </template>
                <template #cell(cert)="row">
                  <CertBadge :data="row.item"></CertBadge>
                </template>
                <template #cell(order_units)="row">
                  <v-select v-model="row.item.order_units" required label="text" placeholder="..." :clearable="false"
                    :options="[
                      { value: 'kilograms', text: 'Kg' },
                      { value: 'pounds', text: 'lb' },
                      { value: 'liters', text: 'L' },
                      { value: 'units', text: 'unit' }
                    ]">
                  </v-select>
                </template>
                <template #cell(price_per)="row">
                  <div class="input-group">
                    <div class="input-group-prepend">
                      <span class="input-group-text">$</span>
                    </div>
                    <b-form-input v-model="row.item.price_per" type="number"
                      aria-describedby="price_per-live-feedback"
                      :disabled="client_purchase"
                      :class="[(client_purchase || (row.item.price_per >= 0 && row.item.price_per !== null) ? '' : 'is-invalid')]"
                    ></b-form-input>
                    <div class="input-group-append">
                      <span class="input-group-text">per {{ row.item.order_units?.text ? row.item.order_units.text : '?' }}</span>
                    </div>
                    <div id="price_per-live-feedback" class="invalid-feedback">This required field must be greater than 0.</div>
                  </div>
                </template>
                <template #cell(order_qty)="row">
                  <div class="input-group">
                    <b-form-input v-model="row.item.order_qty" type="number"
                      aria-describedby="order_qty-live-feedback"
                      :class="[(row.item.order_qty > 0 ? '' : 'is-invalid')]"
                    ></b-form-input>
                    <div class="input-group-append">
                      <span class="input-group-text">{{ row.item.order_units?.text ? row.item.order_units.text + '/s' : '?' }}</span>
                    </div>
                    <div id="order_qty-live-feedback" class="invalid-feedback">This required field must be greater than 0.</div>
                  </div>
                </template>
                <template #cell(details)="row">
                  <b-form-textarea v-model="row.item.details" type="text" rows="1" max-rows="3"></b-form-textarea>
                </template>
              </b-table>
              <div class="m-3">
                <b-button block variant="outline-info" @click="addComponent()">Add Component</b-button>
              </div>
              <div class="d-print-none">
                <h3 id="Documents">Documents</h3>
                <b-card-group class="ml-3">
                  <div v-for="(document, index) in documents" :key="index">
                    <b-card class="m-2 custom_card" style="min-width: 22rem; max-width: 22rem;" no-body>
                      <b-card-body>
                        <b-card-title class="my-1" v-show="document.document_type">
                          {{ document.document_type === 'purchase_order' ? 'Purchase Order' : null }}
                          {{ document.document_type === 'email' ? 'Email' : null }}
                          {{ document.document_type === 'invoice' ? 'Invoice' : null }}
                          {{ document.document_type === 'other' ? 'Other' : null }}
                        </b-card-title>
                        <v-select v-show="!document.document_type" v-model="document.document_type" required label="text" :reduce="doc => doc.value" placeholder="Select Document Type"
                          :options="[
                            { value: 'sale', text: 'Sale' },
                            { value: 'tracking', text: 'Tracking' },
                            { value: 'receipt', text: 'Receipt' },
                            { value: 'email', text: 'Email' },
                            { value: 'invoice', text: 'Invoice' },
                            { value: 'other', text: 'Other' }
                          ]">
                        </v-select>
                        <strong>Document Name: </strong><br><b-form-input v-model="document.name" type="text" class="my-1"></b-form-input>
                        <strong>Description: </strong><br><b-form-textarea v-model="document.description" class="my-1" rows="3" max-rows="3"></b-form-textarea>
                        <b-form-file v-if="!document.file_hash" :disabled="!document.document_type || !document.name" no-drop accept="image/png, image/jpeg, application/pdf" type="file" class="my-2" @change="onFileChange($event, document)"></b-form-file>
                        <b-button :disabled="!document.document_type || !document.name || !document.file_pointer" block :href="getFile(document)" target="_blank" class="btn-light">View Document</b-button>
                      </b-card-body>
                      <b-card-footer>
                        <b-button block :disabled="!document.document_type || !document.name" variant="outline-danger" @click="deleteDocument(document)">Delete Document</b-button>
                      </b-card-footer>
                    </b-card>
                  </div>
                  <b-card class="m-2 custom_card" style="min-width: 22rem; max-width: 22rem; cursor: pointer;" @click="addDocument()">
                    <b-card-title>Add Document</b-card-title>
                  </b-card>
                </b-card-group>
              </div>
              <div class="mt-3">
                <b-button :disabled="!(selected_components.length > 0)" class="mr-2" variant="outline-success" @click="saveOrder()">Save</b-button>
                <b-button variant="outline-danger" to="/orders/po">Cancel</b-button>
              </div>
            </div>
          </div>
        </b-form>
      </div>
    </div>
 </div>
</template>

<style scoped>
.select_org_card {
  width: 50%;
}
.custom_card {
  box-shadow: 0 2px 2px rgba(0,0,0,.2);
}
.my_component {
    width: 90%;
}
@media (max-width: 1024px) {
    .my_component {
      width: 98%;
    }
    .select_org_card {
      width: 100%;
    }
}
@media (max-width: 400px) {
    .my_component {
        width: 100%;
    }
}
</style>

<script>
import ChooseOrg from '@/components/ChooseOrg.vue'
import CertBadge from '@/components/CertBadge.vue'
import ChooseComponent from '@/components/ChooseComponent.vue'
import { CustomRequest, genTempKey } from '../../../common/CustomRequest.js'
import vSelect from 'vue-select'

export default {
  name: 'NewPurchaseOrder',
  components: {
    CertBadge,
    ChooseOrg,
    ChooseComponent,
    vSelect
  },
  data: function () {
    return {
      isMd: false,
      suppliers: [],
      force_loaded: true,
      selected_supplier_buffer: null,
      selected_supplier: null,
      supplier_selected: false,
      components: [],
      selected_components: [],
      documents: [],
      order_buffer: {
        order_date: new Date(),
        supplier_so: '',
        eta_date: null,
        tracking: ''
      },
      req: new CustomRequest(this.$cookies.get('session')),
      del_url_previews: [],
      client_purchase: false,
      clients: [],
      selected_client_buffer: null,
      selected_client: null,
      client_selected: false
    }
  },
  computed: {
    loaded: function () {
      if (this.force_loaded) {
        return this.suppliers.length > 0
      }
      return false
    }
  },
  methods: {
    handleVisible: function (isVisible) {
      this.isMd = isVisible
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
    deleteDocument: function (document) {
      this.documents.splice(this.documents.findIndex((d) => d.id === document.id), 1)
      this.req.deleteFile(document.file_pointer)
    },
    addDocument: function () {
      const document = {
        id: genTempKey(),
        description: null,
        name: null,
        type: `orders/po/${this.selected_supplier.organization_primary_name}/${this.order_buffer.supplier_so}/`,
        id_code: `${this.order_buffer.supplier_so}_`,
        file_pointer: null,
        file_preview_pointer: null,
        file_type: null,
        url_preview: null,
        file_hash: null,
        date_uploaded: null
      }
      this.documents.push(document)
    },
    validateOrder: function () {
      this.$bvToast.hide()

      const errorToast = {
        title: 'Invalid Order',
        message: '',
        variant: 'warning',
        visible: true,
        no_close_button: false,
        no_auto_hide: true,
        auto_hide_delay: false
      }
      const createToast = this.$root.createToast
      let valid = true

      if (this.order_buffer.supplier_so.length === 0) {
        errorToast.message = 'Supplier SO is a required field.'
        createToast(errorToast)
        valid = false
      }

      if (this.order_buffer.order_date === null) {
        errorToast.message = 'Order Date is a required field.'
        createToast(errorToast)
        valid = false
      }

      for (let i = 0; i < this.selected_components.length; i++) {
        const product = this.selected_components[i]
        if (product.component_id === null) {
          errorToast.message = 'Component is a required field.'
          createToast(errorToast)
          valid = false
        }
        if (product.order_units === null) {
          errorToast.message = 'Order Units is a required field.'
          createToast(errorToast)
          valid = false
        }
        if (!this.client_purchase && (product.price_per === null || product.price_per <= 0)) {
          errorToast.message = 'Price Per is a required field and must be greater than 0.'
          createToast(errorToast)
          valid = false
        }
        if (product.order_qty === null || product.order_qty <= 0) {
          errorToast.message = 'Order Quantity is a required field and must be greater than 0.'
          createToast(errorToast)
          valid = false
        }
      }

      // must upload at least one document
      let hasDocument = false
      for (let i = 0; i < this.documents.length; i++) {
        if (this.documents[i].file_pointer) {
          hasDocument = true
          break
        }
      }
      if (!hasDocument) {
        errorToast.message = 'At least one document must be uploaded.'
        createToast(errorToast)
        valid = false
      }

      return valid
    },
    saveOrder: function () {
      this.force_loaded = false
      if (!this.validateOrder()) {
        this.force_loaded = true
        return
      }

      // Prepare request
      const purchaseOrderId = genTempKey()

      for (let i = 0; i < this.selected_components.length; i++) {
        const component = this.selected_components[i]

        let kilosOrderQty = null
        let unitsOrderQty = null
        let litersOrderQty = null
        let bidPricePerUnit = null
        let bidPricePerKilo = null
        let bidPricePerLiter = null

        if (component.order_units.value === 'kilograms') {
          kilosOrderQty = component.order_qty
          bidPricePerKilo = component.price_per
        } else if (component.order_units.value === 'pounds') {
          kilosOrderQty = Math.round(component.order_qty * 2.205, 4)
          bidPricePerKilo = Math.round(component.price_per * 2.205, 4)
        } else if (component.order_units.value === 'liters') {
          litersOrderQty = component.order_qty
          bidPricePerLiter = component.price_per
        } else if (component.order_units.value === 'units') {
          unitsOrderQty = component.order_qty
          bidPricePerUnit = component.price_per
        }

        const purchaseOrderDetail = {
          po_id: purchaseOrderId,
          po_detail_id: genTempKey(),
          timestamp_fetched: new Date().toISOString(),
          component_id: component.component_id,
          order_units: component.order_units.value,
          order_qty: component.order_qty,
          price_per: component.price_per,
          details: component.details,
          kilos_order_qty: kilosOrderQty,
          units_order_qty: unitsOrderQty,
          liters_order_qty: litersOrderQty,
          bid_price_per_unit: bidPricePerUnit,
          bid_price_per_kilo: bidPricePerKilo,
          bid_price_per_liter: bidPricePerLiter
        }
        this.req.upsertRecord('Purchase_Order_Detail', purchaseOrderDetail)
      }

      const purchaseOrder = {
        po_id: purchaseOrderId,
        organization_id: this.selected_supplier.organization_id,
        supplier_so_num: this.order_buffer.supplier_so,
        order_date: new Date(this.order_buffer.order_date).toISOString().split('T')[0],
        eta_date: this.order_buffer.eta_date ? new Date(this.order_buffer.eta_date).toISOString().split('T')[0] : null,
        timestamp_fetched: new Date().toISOString(),
        doc: {
          purchase_order_files: this.documents
        }
      }
      this.req.upsertRecord('Purchase_Orders', purchaseOrder)

      this.req.sendRequest(this.$root.getOrigin()).then(resp => {
        const createToast = this.$root.createToast
        resp.messages.flash.forEach(message => {
          createToast(message)
        })

        if (resp.status === 201) {
          Object.values(resp.data[0].temp_key_lookup).forEach(item => {
            if (item.table_name === 'Purchase_Orders') {
              this.$router.push({ path: `/orders/po/${item.new_id}` })
            }
          })
        }
      })

      this.force_loaded = true
    },
    updateComponent: function (component, c, index) {
      const update = {
        ...component,
        ...c
      }
      this.selected_components.splice(index, 1, update)
      return update
    },
    removeComponent: function (index) {
      this.selected_components.splice(index, 1)
    },
    addComponent: function () {
      this.selected_components.push({
        component_id: null,
        component_name: null,
        component_primary_name: null,
        order_units: null,
        order_qty: null,
        price_per: null,
        details: null
      })
    },
    getComponents: function () {
      const fetchRequest = this.$root.getOrigin() + '/api/v1/organizations?populate=supplies&org-id=' + this.selected_supplier.organization_id
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
            this.components = data.data[0].supplies
            // eslint-disable-next-line
            console.log(this.components)
          })
        } else if (response.status === 401) {
          this.$router.push({
            name: 'login'
          })
        } else if (response.status === 404) {
          const createToast = this.$root.createToast
          const message = {
            title: 'No Components Found',
            message: 'No components found for this supplier. Please add components to the supplier before creating an order.',
            variant: 'danger'
          }
          createToast(message)
          this.selected_supplier = null
          this.supplier_selected = false
        } else {
          // eslint-disable-next-line
          console.log('Looks like there was a problem. Status Code:' + response.status)
          // eslint-disable-next-line
          console.log(response)
        }
      })
    },
    setSupplier: function () {
      this.selected_supplier = this.selected_supplier_buffer
      this.supplier_selected = true
      this.getComponents()
    },
    getSuppliers: async function () {
      const fetchRequest = '/api/v1/organizations?org-type=supplier'
      const resp = await this.$root.getData(fetchRequest)
      this.suppliers = resp.data
      this.loaded = true
    },
    getClients: async function () {
      if (this.clients.length !== 0) {
        return
      }
      const fetchRequest = '/api/v1/organizations?org-type=client'
      const resp = await this.$root.getData(fetchRequest)
      this.clients = resp.data
    },
    setClient: function () {
      if (!this.client_purchase) {
        return
      }
      this.selected_client = this.selected_client_buffer
      this.client_selected = true
    }
  },
  created: function () {
    this.getSuppliers()
    this.addComponent()
  }
}
</script>

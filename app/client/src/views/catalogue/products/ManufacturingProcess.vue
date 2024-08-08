<template>
  <b-overlay :show="overlay" :opacity="1" rounded="sm">
    <b-card :id="'my_node-'+node_buffer.data.process_spec_id" style="width: fit-content; min-width: 300px; min-height:300px;">
      <b-card-title v-if="node_buffer.data.manufacturing_process_id">{{ node_buffer.data.process_name }}{{ variant?.variant_title ? ' - ' + variant.variant_title : '' }}<b-badge v-show="variant?.discontinued" class="ml-3" variant="danger">Discontinued</b-badge></b-card-title>
      <b-card-title v-else>
        New Process
      </b-card-title>
      <b-card-sub-title class="mb-3">{{ node_buffer.data.process_sop }}</b-card-sub-title>
      <b-card-text class="flex-d justify-content-center">
        <b-container class="m-0 p-0" style="min-width:100%;" v-if="node_buffer.data.manufacturing_process_id">
          <b-row class="mb-3">
            <b-col v-if="!node_buffer.data.manufacturing_process_id">
              <ChooseProcess
                @process="(pro) => updateProcess(pro)"
                :processes="process_options"
                :selected="getProcess()"
                :process-req="true"
              ></ChooseProcess>
            </b-col>
          </b-row>
          <b-row class="mb-3" v-if="node_buffer.data.requires_product_variant">
            <b-col v-if="!node_buffer.data.variant_id && edit">
              <ChooseVariant
                @variant="(variant) => updateVariant(variant)"
                :variants="variant_options"
                :selected="variant"
                :variant-req="true"
              ></ChooseVariant>
            </b-col>
            <b-col v-else>
              <p><strong>Variant:  </strong>{{ variant?.variant_title }}</p>
            </b-col>
          </b-row>
          <b-row class="mb-3">
            <b-col>
              <strong>Special Instructions:</strong>
              <p style="">{{ node_buffer.data.special_instruction }}</p>
              <b-form-textarea
                  :disabled="!edit"
                  id="textarea"
                  v-model="node_buffer.data.special_instruction"
                  placeholder="Special Instruction..."
                  rows="3"
                  max-rows="6"
                ></b-form-textarea>
            </b-col>
          </b-row>
          <b-row v-if="!edit" class="mb-3" v-show="node_buffer.data.requires_components">
            <b-col>
              <b-table :items="node_buffer.data.process_components" :fields="component_fields" striped bordered sticky-header head-variant="light" style="max-height: 600px; min-width: 1100px;" show-empty :empty-text="'No Components Selected for this Process'">
                <template #cell(components)="components">
                  <div v-for="(comp, index) in components.value" :key="comp.component_id+'-components'">
                    <b-row align-v="baseline" class="flex-nowrap">
                      <b-col cols="1">
                        <b-badge :id="comp.component_id+'-components-priority'" v-bind:variant="(comp.priority === 1 ? 'primary' : 'light')" pill class="ml-2 mt-3">{{ comp.priority }}</b-badge>
                        <b-tooltip :target="comp.component_id+'-components-priority'" triggers="hover">Priority Level: {{ comp.priority }}</b-tooltip>
                      </b-col>
                      <b-col cols="6"><b-link :to="'/catalogue/components/'+comp.component_id" target="_blank"><p class="py-3">{{ comp.component_primary_name ? comp.component_primary_name : comp.component_name }}</p></b-link></b-col>
                      <b-col><CertBadge :data="comp"></CertBadge></b-col>
                    </b-row>
                    <hr v-show="index < components.value.length-1">
                  </div>
                </template>
                <template #cell(brands)="brands">
                  <div v-for="(brand, index) in brands.value" :key="brand.organization_id+'-org'">
                    <p class="py-3">
                      <b-badge :id="brand.organization_id+'-org-priority'" v-bind:variant="(brand.priority === 1 ? 'primary' : 'light')" pill class="mr-2">{{ brand.priority }}</b-badge>
                      <b-tooltip :target="brand.organization_id+'-org-priority'" triggers="hover">Priority Level: {{ brand.priority }}</b-tooltip>
                      <span :id="brand.organization_id+'-org-name'">{{ brand.organization_initial }}</span>
                      <b-tooltip :target="brand.organization_id+'-org-name'" triggers="hover">{{ brand.organization_name }}</b-tooltip>
                    </p>
                    <hr v-show="index < brands.value.length-1">
                  </div>
                </template>
                <template #cell(qty_per_unit)="qty_per_unit">
                  <strong style="font-size: 1.5em;">{{ qty_per_unit.value }}</strong>
                </template>
                <template #cell(specific_brand_required)="specific_brand_required">
                  <span v-if="specific_brand_required.value" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</span>
                  <span v-else class="badge badge-warning badge-pill" style="font-size: 1.5em;">No</span>
                </template>
                <template #cell(specific_component_required)="specific_component_required">
                  <span v-if="specific_component_required.value" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</span>
                  <span v-else class="badge badge-warning badge-pill" style="font-size: 1.5em;">No</span>
                </template>
              </b-table>
            </b-col>
          </b-row>
          <b-row v-else v-show="node_buffer.data.requires_components">
            <b-col>
              <b-table :items="node_buffer.data.process_components" :fields="component_fields" striped bordered sticky-header head-variant="light" style="max-height: 600px; min-width: 1100px;" show-empty :empty-text="'No Components Selected for this Process'">
                <template #cell(components)="components">
                  <div v-for="(comp, index) in components.value" :key="comp.component_id+'-component'">
                    <b-row align-v="baseline" class="flex-nowrap">
                      <b-col style="margin: 5px; padding: 0px; margin-left: 10px; max-width: 22px;">
                        <b-badge :id="components.item.process_component_id+'-'+comp.component_id+'-component-priority'" v-bind:variant="(comp.priority === 1 ? 'primary' : 'light')" pill>{{ comp.priority }}</b-badge>
                        <b-tooltip :target="components.item.process_component_id+'-'+comp.component_id+'-component-priority'" triggers="hover">Priority Level: {{ comp.priority }}</b-tooltip>
                      </b-col>
                      <b-col style="padding: 0px; margin: 10px; max-width: 48px;">
                        <b-button @click="removeComp(components.value, components.index, index)" variant="outline-danger"><b-icon icon="trash"></b-icon></b-button>
                      </b-col>
                      <b-col style="min-width: 400px;">
                        <ChooseComponent
                          class="py-3"
                          @comp="(c) => selectComp(c, components.item.components, index)"
                          :components="component_options" :selected="comp.component_id === 0 ? null : comp"
                        ></ChooseComponent>
                      </b-col>
                    </b-row>
                    <hr v-show="index < components.value.length">
                  </div>
                  <div class="d-flex justify-content-end">
                    <b-button variant="outline-info" @click="addComp(components.item.process_component_id, components.item.components)" class="mr-3">Add Component</b-button>
                    <b-button variant="outline-danger" @click="deleteRow(components.index)">Delete Row</b-button>
                  </div>
                </template>
                <template #cell(brands)="brands">
                  <div v-for="(brand, index) in brands.value" :key="brand.organization_id+'-org'">
                    <b-row align-v="baseline" class="flex-nowrap">
                      <b-col style="margin: 5px; padding: 0px; margin-left: 10px; max-width: 22px;">
                        <b-badge :id="brands.item.process_component_id+'-'+brand.organization_id+'-org-priority'" v-bind:variant="(brand.priority === 1 ? 'primary' : 'light')" pill>{{ brand.priority }}</b-badge>
                        <b-tooltip :target="brands.item.process_component_id+'-'+brand.organization_id+'-org-priority'" triggers="hover">Priority Level: {{ brand.priority }}</b-tooltip>
                      </b-col>
                      <b-col style="padding: 0px; margin: 10px; max-width: 48px;">
                        <b-button @click="removeBrand(brands.value, brands.index, index)" variant="outline-danger"><b-icon icon="trash"></b-icon></b-button>
                      </b-col>
                      <b-col>
                        <ChooseOrg
                          @org="(o) => selectBrand(o, brands.item.brands, index)"
                          :organizations="brand_options"
                          :selected="brand.organization_id === 0 ? null : brand"
                          :org-req="brands.item.specific_brand_required"
                        ></ChooseOrg>
                      </b-col>
                    </b-row>
                    <hr v-show="index < brands.value.length">
                  </div>
                  <div class="d-flex justify-content-end mt-2">
                    <b-button variant="outline-info" @click="addBrand(brands.item.process_component_id, brands.item.brands)">Add Brand</b-button>
                  </div>
                </template>
                <template #cell(qty_per_unit)="qty_per_unit">
                  <div class="input-group mb-2" style="font-size: 1.5em; width: 80px;">
                    <strong>
                      <input
                      :id="qty_per_unit.item.process_component_id+'-qty_per_unit'"
                      type="number" class="form-control"
                      v-model="qty_per_unit.item.qty_per_unit"
                      required
                      min="0"
                      aria-describedby="qty_per_unit-live-feedback"
                      :class="['form-control', (qty_per_unit.item.qty_per_unit > 0 ? '' : 'is-invalid')]"
                      @input="updateRow(qty_per_unit.item)"
                    >
                    </strong>
                    <div :id="qty_per_unit.item.process_component_id+'-qty_per_unit-live-feedback'" class="invalid-feedback">This required field must be greater than zero.</div>
                  </div>
                </template>
                <template #cell(specific_brand_required)="specific_brand_required">
                  <b-button @click="specific_brand_required.item.specific_brand_required = false;updateRow(specific_brand_required.item)" v-show="specific_brand_required.value" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</b-button>
                  <b-button @click="specific_brand_required.item.specific_brand_required = true;updateRow(specific_brand_required.item)" v-show="!specific_brand_required.value" class="badge badge-warning badge-pill" style="font-size: 1.5em;">No</b-button>
                </template>
                <template #cell(specific_component_required)="specific_component_required">
                  <b-button @click="specific_component_required.item.specific_component_required = false;updateRow(specific_component_required.item)" v-show="specific_component_required.value" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</b-button>
                  <b-button @click="specific_component_required.item.specific_component_required = true;updateRow(specific_component_required.item)" v-show="!specific_component_required.value" class="badge badge-warning badge-pill" style="font-size: 1.5em;">No</b-button>
                </template>
              </b-table>
            </b-col>
          </b-row>
          <b-row class="mb-3" v-if="edit" v-show="node_buffer.data.requires_components">
            <b-col>
              <b-button v-show="edit" block variant="outline-info" @click="addRow()">Add Row</b-button>
            </b-col>
          </b-row>
          <b-row class="mb-3">
            <b-col>
              <b-table :items="sortEquipment(node_buffer.data.equipment)" :fields="equipment_fields" striped bordered sticky-header head-variant="light" style="max-height: 600px; min-width: 1100px;" show-empty :empty-text="'No Equipment Needed for this Process'">
                <template #cell(equipment_name)="equipment_name">
                  <b-button v-on:click.stop class="mr-2" variant="light" :to="'/manufacturing/equipment/'+equipment_name.item.equipment_id" target="_blank"><b-icon icon="box"></b-icon></b-button>
                  <b class="text-info">{{ equipment_name.value }}</b>
                </template>
                <template #cell(status)="status">
                  <h4 v-if="status.value === 'Working_Order'"><b-badge variant="success">{{ status.value.replace('_', ' ') }}</b-badge></h4>
                  <h4 v-if="status.value === 'Broken'"><b-badge variant="danger">{{ status.value.replace('_', ' ') }}</b-badge></h4>
                  <h4 v-if="status.value === 'Removed'"><b-badge variant="light">{{ status.value.replace('_', ' ') }}</b-badge></h4>
                </template>
              </b-table>
            </b-col>
          </b-row>
        </b-container>
      </b-card-text>
      <Handle v-if="node_buffer.data.top_handle" id="a" type="target" class="custom_vue-flow__handle" :position="top" />
      <Handle v-if="node_buffer.data.bottom_handle" id="b" type="source" class="custom_vue-flow__handle" :position="bottom" />
      <NodeToolbar :is-visible="node_data.toolbarVisible" :position="bottom" :align="'end'">
        <b-button v-show="edit" variant="outline-danger" @click="deleteNode()">Delete Process</b-button>
      </NodeToolbar>
    </b-card>
    <template #overlay>
      <div class="text-center" style="width: 100%;">
        <strong style="font-size: 6em;">{{ node_buffer.data.process_name }}{{ variant?.variant_title ? ' - ' + variant.variant_title : '' }}</strong>
        <b-badge style="font-size: 6em;" v-show="variant?.discontinued" class="ml-3" variant="danger">Discontinued</b-badge>
      </div>
    </template>
  </b-overlay>
</template>

<style scoped>
.btn {
  white-space: nowrap
}
.custom_vue-flow__handle {
  width: 16px;
  height: 16px;
}
.card {
  box-shadow: 0 10px 10px rgba(0,0,0,.2);
}
.custom-row {
  border-bottom-width: thick !important;
  border-top-width: thick !important;
}
</style>

<script>
import { Handle, Position } from '@vue-flow/core'
import { NodeToolbar } from '@vue-flow/node-toolbar'
import CertBadge from '../../../components/CertBadge.vue'
import { genTempKey } from '../../../common/CustomRequest.js'
import { cloneDeep } from 'lodash'
import ChooseComponent from '../../../components/ChooseComponent.vue'
import ChooseOrg from '../../../components/ChooseOrg.vue'
import ChooseProcess from '../../../components/ChooseProcess.vue'
import ChooseVariant from '../../../components/ChooseVariant.vue'

export default {
  data: function () {
    return {
      right: Position.Right,
      left: Position.Left,
      top: Position.Top,
      bottom: Position.Bottom,
      node_buffer: null,
      component_fields: [
        { label: 'Component', key: 'components', tdClass: 'custom-row' },
        { label: 'Brands', key: 'brands', tdClass: 'custom-row' },
        { label: 'Qty', key: 'qty_per_unit', tdClass: ['align-middle', 'custom-row'], class: 'text-center' },
        { label: 'Brand Specific', key: 'specific_brand_required', tdClass: ['align-middle', 'custom-row'], class: 'text-center' },
        { label: 'Component Specific', key: 'specific_component_required', tdClass: ['align-middle', 'custom-row'], class: 'text-center' }
      ],
      equipment_fields: [
        { label: 'Equipment', key: 'equipment_name' },
        { label: 'Serial No.', key: 'equipment_sn' },
        { label: 'Status', key: 'status' }
      ],
      variant: null
    }
  },
  props: {
    node_data: {
      required: true,
      type: Object
    },
    edit: {
      required: true,
      type: Boolean
    },
    id: {
      required: true
    },
    component_options: {
      required: true,
      type: Array
    },
    brand_options: {
      required: true,
      type: Array
    },
    process_options: {
      required: true,
      type: Array
    },
    variant_options: {
      required: true,
      type: Array
    },
    overlay: {
      required: true,
      type: Boolean
    }
  },
  components: {
    Handle,
    NodeToolbar,
    CertBadge,
    ChooseComponent,
    ChooseOrg,
    ChooseProcess,
    ChooseVariant
  },
  methods: {
    getVariant: function () {
      if (this.variant !== null) {
        return
      }
      if (!this.node_buffer.data.variant_id) {
        this.variant = null
        return
      }
      this.variant = this.variant_options.find((v) => v.variant_id === this.node_buffer.data.variant_id)
    },
    updateVariant: function (variant) {
      this.variant = variant
      this.node_buffer.data.variant_id = variant.variant_id
      this.updateNode()
    },
    removeBrand: function (brands, rowIndex, brandIndex) {
      this.$emit('deleteNodeRowBrand', cloneDeep(this.node_buffer.data), rowIndex, brandIndex)
      for (let i = brandIndex; i < brands.length; i++) {
        brands[i].priority = i + 1
      }
    },
    selectBrand: function (org, brands, index) {
      if (org !== null) {
        const brand = {
          _id: brands[index]._id,
          brand_id: org.organization_id,
          priority: brands[index].priority,
          process_component_id: brands[index].process_component_id,
          ...org
        }
        brands[index] = brand
        this.updateRow()
      }
    },
    addBrand: function (processComponentId, brands) {
      const newBrand = {
        _id: genTempKey(),
        process_component_id: processComponentId,
        brand_id: 0,
        priority: brands.length + 1
      }
      brands.push(newBrand)
      this.updateRow()
    },
    removeComp: function (components, rowIndex, compIndex) {
      this.$emit('deleteNodeRowComponent', cloneDeep(this.node_buffer.data), rowIndex, compIndex)
      for (let i = compIndex; i < components.length; i++) {
        components[i].priority = i + 1
      }
    },
    selectComp: function (comp, components, index) {
      if (comp !== null) {
        const component = {
          _id: components[index]._id,
          component_id: comp.component_id,
          priority: components[index].priority,
          process_component_id: components[index].process_component_id,
          ...comp
        }
        components[index] = component
        this.updateRow()
      }
    },
    addComp: function (processComponentId, components) {
      const newComponent = {
        _id: genTempKey(),
        process_component_id: processComponentId,
        component_id: 0,
        priority: components.length + 1
      }
      components.push(newComponent)
      this.updateRow()
    },
    deleteRow: function (index) {
      this.$emit('deleteNodeRow', cloneDeep(this.node_buffer.data), index)
    },
    updateRow: function () {
      this.updateNode()
    },
    addRow: function () {
      const processComponentId = genTempKey()
      const newRow = {
        process_spec_id: this.id,
        process_component_id: processComponentId,
        qty_per_unit: 0,
        specific_brand_required: false,
        specific_component_required: false,
        components: [
          {
            _id: genTempKey(),
            process_component_id: processComponentId,
            component_id: 0,
            priority: 1
          }
        ],
        brands: []
      }
      this.node_buffer.data.process_components.push(newRow)
      this.updateNode()
    },
    sortEquipment: function (equipment) {
      return equipment.sort((a, b) => {
        if (a.status === b.status) {
          return 0
        } else if ((a.status === 'Working_Order' && b.status !== 'Working_Order') || b.status === 'Removed') {
          return -1
        } else {
          return 1
        }
      })
    },
    updateProcess: function (newProcess) {
      this.node_buffer.data = {
        ...this.node_buffer.data,
        ...cloneDeep(newProcess)
      }
      this.node_buffer.data.manufacturing_process_id = newProcess.process_id
      this.updateNode()
    },
    getProcess: function () {
      const processData = {
        process_id: this.node_buffer.data.manufacturing_process_id,
        process_name: this.node_buffer.data.process_name,
        process_sop: this.node_buffer.data.process_sop
      }
      return processData
    },
    updateNode: function () {
      this.$nextTick(() => {
        this.$emit('updateNodeData', this.node_buffer.data)
      })
    },
    deleteNode: function () {
      this.$emit('deleteNode', this.node_buffer.data)
    }
  },
  created: function () {
    this.node_buffer = cloneDeep(this.node_data)
    this.getVariant()
  }
}
</script>

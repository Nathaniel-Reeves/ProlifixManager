<template>
  <b-overlay :show="true" :opacity="1" rounded="sm" style="white-space: nowrap;">
    <b-card :id="'my_node-'+node_buffer.data.process_spec_id" style="min-width: 800px; max-width: 1000px; min-height:200px; box-shadow: 0 10px 10px rgba(0,0,0,.2) !important;">
      <b-card-title>
        <b-badge v-show="variant?.discontinued" class="ml-3" variant="danger">Discontinued</b-badge>
        <b-badge v-show="node_buffer.data.primary_process && !edit" class="ml-3" variant="primary">Primary</b-badge>
      </b-card-title>
      <b-card-sub-title class="mb-3"><b-link :href="node_buffer.data.process_sop_link" target="_blank" class="text-info">{{ node_buffer.data.process_sop }}</b-link></b-card-sub-title>
      <Handle v-if="node_buffer.data.top_handle" id="a" type="target" class="custom_vue-flow__handle" :position="top" />
      <Handle v-if="node_buffer.data.bottom_handle" id="b" type="source" class="custom_vue-flow__handle" :position="bottom" />
    </b-card>
    <template #overlay>
      <div class="text-center" style="width: 100%;">
        <strong style="font-size: 3.5em;">{{ node_buffer.data.process_name }}{{ variant?.variant_title ? ' - ' + variant.variant_title : '' }}</strong>
        <!-- <b-badge style="font-size: 4em;" v-show="variant?.discontinued" class="ml-3" variant="danger">Discontinued</b-badge>
        <b-badge style="font-size: 4em;" v-show="node_buffer.data.primary_process" class="ml-3" variant="primary">Primary</b-badge> -->
      </div>
    </template>
  </b-overlay>
</template>

<style scoped>
.btn {
  white-space: nowrap
}
.custom_vue-flow__handle {
  width: 1px;
  height: 1px;
}
.custom-row {
  border-bottom-width: thick !important;
  border-top-width: thick !important;
}
</style>

<script>
import { Handle, Position } from '@vue-flow/core'
import { genTempKey } from '../../../common/CustomRequest.js'
import { cloneDeep } from 'lodash'

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
      variant: null,
      show_variant: false
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
    Handle
  },
  methods: {
    toggleShowVariant: function () {
      this.show_variant = !this.show_variant
      // wait 1 second before resizing node
      setTimeout(() => {
        this.$emit('resizeNode', this.node_buffer.data)
      }, 1000)
    },
    toggleDefaultPercentLoss: function () {
      this.node_buffer.data.use_default_ave_percent_loss = !this.node_buffer.data.use_default_ave_percent_loss
      if (this.node_buffer.data.use_default_ave_percent_loss) {
        this.node_buffer.data.custom_ave_percent_loss = this.node_buffer.data.ave_percent_loss
      }
      this.updateNode()
    },
    toggleDefaultSetup: function () {
      this.node_buffer.data.custom_setup_time_use_default = !this.node_buffer.data.custom_setup_time_use_default
      if (this.node_buffer.data.custom_setup_time_use_default) {
        this.node_buffer.data.custom_setup_time = this.node_buffer.data.setup_time
        this.node_buffer.data.custom_setup_time_units = this.node_buffer.data.setup_time_units
        this.node_buffer.data.custom_setup_num_employees = this.node_buffer.data.setup_num_employees
      }
      this.updateNode()
    },
    toggleDefaultCleanup: function () {
      this.node_buffer.data.custom_cleaning_time_use_default = !this.node_buffer.data.custom_cleaning_time_use_default
      if (this.node_buffer.data.custom_cleaning_time_use_default) {
        this.node_buffer.data.custom_cleaning_time = this.node_buffer.data.cleaning_time
        this.node_buffer.data.custom_cleaning_time_units = this.node_buffer.data.cleaning_time_units
        this.node_buffer.data.custom_cleaning_num_employees = this.node_buffer.data.cleaning_num_employees
      }
      this.updateNode()
    },
    updateBox: function (box) {
      this.node_buffer.data.box_id = box.component_id
      this.updateNode()
    },
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
          ...org,
          timestamp_fetched: org.timestamp_fetched
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
        priority: brands.length + 1,
        timestamp_fetched: new Date().toISOString()
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
          ...comp,
          timestamp_fetched: comp.timestamp_fetched
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
        priority: components.length + 1,
        timestamp_fetched: new Date().toISOString()
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
        brands: [],
        timestamp_fetched: new Date().toISOString()
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
      if (this.node_buffer.data.use_default_ave_percent_loss) {
        this.node_buffer.data.custom_ave_percent_loss = this.node_buffer.data.ave_percent_loss
      }
      if (this.node_buffer.data.custom_setup_time_use_default) {
        this.node_buffer.data.custom_setup_time = this.node_buffer.data.setup_time
        this.node_buffer.data.custom_setup_time_units = this.node_buffer.data.setup_time_units
        this.node_buffer.data.custom_setup_num_employees = this.node_buffer.data.setup_num_employees
      }
      if (this.node_buffer.data.custom_cleaning_time_use_default) {
        this.node_buffer.data.custom_cleaning_time = this.node_buffer.data.cleaning_time
        this.node_buffer.data.custom_cleaning_time_units = this.node_buffer.data.cleaning_time_units
        this.node_buffer.data.custom_cleaning_num_employees = this.node_buffer.data.cleaning_num_employees
      }
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
  computed: {
    box_options: function () {
      if (!this.component_options) {
        return []
      }
      return this.component_options.filter((c) => c.component_type === 'box')
    },
    box: function () {
      if (!this.node_buffer.data.box_id) {
        return null
      }
      return this.component_options.find((c) => c.component_id === this.node_buffer.data.box_id)
    },
    filteredVariantOptions: function () {
      if (this.node_buffer.data.product_variant_type === null) {
        return this.variant_options
      }
      return this.variant_options.filter(variant => variant.variant_type === this.node_buffer.data.product_variant_type)
    },
    filtered_component_options: function () {
      if (!this.component_options) {
        return []
      }
      if (!this.node_buffer.component_filters) {
        return this.component_options
      }
      const filter = this.node_buffer.data.component_filters
      return this.component_options.filter((c) => filter.indexOf(c.component_type) > -1)
    }
  },
  created: function () {
    this.node_buffer = cloneDeep(this.node_data)
    this.getVariant()
  }
}
</script>

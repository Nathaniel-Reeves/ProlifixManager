<template>
  <b-card>
    <b-card-title>{{ process.process_name }}</b-card-title>
    <b-card-sub-title class="mb-3">{{ process.process_sop }}</b-card-sub-title>
    <b-card-text>
      <b-table-lite :items="process.components" :fields="fields" stacked="md" striped bordered v-if="process.components.length > 0">
        <template #cell(components)="components">
          <div v-for="(comp, index) in components.value" :key="comp.component_id+'-components'">
            <b-row style="height:80px;">
              <b-col cols="1">
                <b-badge :id="comp.component_id+'-components-priority'" v-bind:variant="(comp.priority === 1 ? 'primary' : 'light')" pill class="ml-2 mt-3">{{ comp.priority }}</b-badge>
                <b-tooltip :target="comp.component_id+'-components-priority'" triggers="hover">Priority Level: {{ comp.priority }}</b-tooltip>
              </b-col>
              <b-col cols="6"><b-link :to="'/catalogue/components/'+comp.component_id" target="_blank"><p class="py-3">{{ comp.component_name }}</p></b-link></b-col>
              <b-col><CertBadge :data="comp"></CertBadge></b-col>
            </b-row>
            <hr v-show="index < components.value.length-1">
          </div>
        </template>
        <template #cell(brands)="brands">
          <div v-for="(brand, index) in brands.value" :key="brand.organization_id+'-org'">
            <p class="py-3" style="height:80px;">
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
      </b-table-lite>
      <b-container>
        <b-row>
          <b-col>
            <strong>Special Instructions:</strong>
            <p style="">{{ process.special_instruction }}</p>
        </b-col>
        </b-row>
        <b-row>
          <b-col>
            <strong class="mb-2">Equipment:</strong>
            <b-list-group>
              <b-list-group-item v-for="e in process.equipment" :key="e.equipment_id">{{ e.equipment_sn }}  <b-badge variant="warning" v-show="e.status != 'Working_Order'">!</b-badge></b-list-group-item>
            </b-list-group>
          </b-col>
          <b-col>
            <strong>Bid Pricing:</strong>
            <p>${{ process.process_bid_cost }}/unit   ({{ process.min_personnel }}-{{ process.max_personnel }} persons)</p>
          </b-col>
        </b-row>
      </b-container>
    </b-card-text>
    <Handle id="a" type="target" :position="top" />
    <Handle id="b" type="source" :position="bottom" />
    <NodeToolbar :is-visible="node_data.toolbarVisible" :position="bottom" :align="'end'">
      <b-button variant="outline-info" class="mr-2">Edit</b-button>
      <b-button variant="outline-danger">Delete</b-button>
    </NodeToolbar>
  </b-card>
</template>

<style scoped>
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

export default {
  data: function () {
    return {
      right: Position.Right,
      left: Position.Left,
      top: Position.Top,
      bottom: Position.Bottom,
      process: this.node_data.data,
      edit_manufacturing: false,
      fields: [
        { label: 'Component', key: 'components', tdClass: 'custom-row' },
        { label: 'Brands', key: 'brands', tdClass: 'custom-row' },
        { label: 'Qty', key: 'qty_per_unit', tdClass: ['align-middle', 'custom-row'], class: 'text-center' },
        { label: 'Brand Specific', key: 'specific_brand_required', tdClass: ['align-middle', 'custom-row'], class: 'text-center' },
        { label: 'Component Specific', key: 'specific_component_required', tdClass: ['align-middle', 'custom-row'], class: 'text-center' }
      ]
    }
  },
  props: {
    node_data: {
      required: true,
      type: Object
    },
    id: {
      required: true
    }
  },
  components: {
    Handle,
    NodeToolbar,
    CertBadge
  }
}
</script>

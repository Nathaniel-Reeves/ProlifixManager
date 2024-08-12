<template>
  <b-overlay id="Manufacturing" :show="loading" :opacity="0.75">
    <h3>Manufacturing<b-button v-if="!edit_manufacturing" v-b-tooltip.hover title="Edit Manufacturing Process" v-on:click="setProcessesBuffer()" class="btn p-1 ml-2 btn-light" type="button"><b-icon icon="pencil-square" class="d-print-none"></b-icon></b-button></h3>
    <div class="my_component d-flex flex-wrap justify-content-center">
      <div class="d-flex justify-content-center" style="width: 100%; height: 700px">
        <VueFlow
          @pane-ready="onPaneReady"
          @connect="onConnect"
          @edge-update-end="onEdgeUpdateEnd"
          :nodes="nodes"
          :edges="edges"
          :nodesConnectable="edit_manufacturing"
          :nodesDraggable="edit_manufacturing"
          :max-zoom="2"
          :min-zoom="0.2"
          :zoom-on-double-click="true"
          :no-wheel-class-name="false"
          :prevent-scrolling="false"
        >
          <Background />
          <Panel position="top-right">
            <b-button-group>
              <b-button variant="light" style="border-width: 1px; border-color:#999999" @click="zoomin()"><b-icon icon="zoom-in"></b-icon></b-button>
              <b-button variant="light" style="border-width: 1px; border-color:#999999" @click="zoomout()"><b-icon icon="zoom-out"></b-icon></b-button>
              <b-button variant="light" style="border-width: 1px; border-color:#999999" @click="zoomfit()"><b-icon icon="fullscreen"></b-icon></b-button>
            </b-button-group>
          </Panel>
          <Panel position="bottom-left">
            <div class="d-flex">
              <div style="background-color: white;" class="mr-2" v-show="edit_manufacturing">
                <b-button variant="outline-success" @click="submit()">Save Changes</b-button>
              </div>
              <div style="background-color: white;" class="mr-2" v-show="edit_manufacturing">
                <b-button variant="outline-info" @click="addProcess()">New Process</b-button>
              </div>
              <div style="background-color: white;" class="mr-2" v-show="edit_manufacturing">
                <b-button variant="outline-danger" @click="cancel()">Cancel</b-button>
              </div>
            </div>
          </Panel>
          <MiniMap />
          <template #node-manufacturing-process="node_data">
            <ManufacturingProcess
              :id="node_data.process_spec_id"
              :node_data="node_data"
              :component_options="component_options"
              :brand_options="brand_options"
              :process_options="process_options"
              :variant_options="variant_options"
              :edit="edit_manufacturing"
              :overlay="overlay || loading"
              v-on:resize-node="node => resizeNode(node)"
              v-on:set-graph="layoutGraph()"
              v-on:update-node-data="(node) => updateNodeData(node)"
              v-on:delete-node="(node) => deleteProcess(node)"
              v-on:delete-node-row="(node, rowIndex) => deleteNodeRow(node, rowIndex)"
              v-on:delete-node-row-brand="(node, rowIndex, brandIndex) => deleteNodeRowBrand(node, rowIndex, brandIndex)"
              v-on:delete-node-row-component="(node, rowIndex, compIndex) => deleteNodeRowComponent(node, rowIndex, compIndex)"
            />
          </template>
          <template #edge-button="buttonEdgeProps">
            <BaseEdge :id="buttonEdgeProps.id" style="stroke-width: 6;" :path="getSmoothStepPath({
                id: buttonEdgeProps.id,
                sourceX: buttonEdgeProps.sourceX,
                sourceY: buttonEdgeProps.sourceY,
                targetX: buttonEdgeProps.targetX,
                targetY: buttonEdgeProps.targetY,
                sourcePosition: buttonEdgeProps.sourcePosition,
                targetPosition: buttonEdgeProps.targetPosition
              })[0]" :marker-end="buttonEdgeProps.markerEnd" />
            <EdgeWithButton
              :id="buttonEdgeProps.id"
              :edit="edit_manufacturing"
              :source-x="buttonEdgeProps.sourceX"
              :source-y="buttonEdgeProps.sourceY"
              :target-x="buttonEdgeProps.targetX"
              :target-y="buttonEdgeProps.targetY"
              :source-position="buttonEdgeProps.sourcePosition"
              :target-position="buttonEdgeProps.targetPosition"
              :marker-end="buttonEdgeProps.markerEnd"
              :custom-style="buttonEdgeProps.style"
              v-on:delete-edge="id => deleteEdge(id)"
            />
          </template>
        </VueFlow>
      </div>
    </div>
  </b-overlay>
</template>

<script>
import dagre from '@dagrejs/dagre'
import { Panel, VueFlow, MarkerType, getSmoothStepPath, BaseEdge } from '@vue-flow/core'
import { Background } from '@vue-flow/background'
import { MiniMap } from '@vue-flow/minimap'
import ManufacturingProcess from './ManufacturingProcess.vue'
import { CustomRequest, genTempKey, isTempKey } from '../../../common/CustomRequest.js'
import { cloneDeep } from 'lodash'
import EdgeWithButton from './EdgeWithButton.vue'

export default {
  name: 'ProductManufacturing',
  components: {
    VueFlow,
    MiniMap,
    Background,
    Panel,
    ManufacturingProcess,
    EdgeWithButton,
    BaseEdge
  },
  props: {
    manufacturing: {
      type: Object,
      required: true
    },
    productId: {
      type: Number,
      required: true
    },
    variant_options: {
      type: Array,
      required: true
    }
  },
  data: function () {
    return {
      nodes: [],
      edges: [],
      nodes_buffer: [],
      edges_buffer: [],
      edit_manufacturing: false,
      instance: null,
      req: new CustomRequest(this.$cookies.get('session')),
      component_options: [],
      brand_options: [],
      process_options: [],
      loading: true
    }
  },
  computed: {
    overlay: function () {
      if (this.instance === null) {
        return true
      }
      return this.instance.getViewport().zoom < 0.5
    }
  },
  methods: {
    getSmoothStepPath: function (path) {
      return getSmoothStepPath(path)
    },
    deleteNodeRowBrand: function (nodeData, rowIndex, brandIndex) {
      const nodeIndex = this.nodes_buffer.findIndex((n) => n.process_spec_id === nodeData.process_spec_id)
      const row = this.nodes_buffer[nodeIndex].process_components[rowIndex]
      const brand = row.brands.splice(brandIndex, 1)[0]
      if (isTempKey(brand._id)) {
        this.req.removeUpsertRecord('Component_Brands_Join', '_id', brand._id)
      } else {
        this.req.deleteRecord('Component_Brands_Join', { _id: brand._id })
      }
      for (let i = brandIndex; i < row.brands.length; i++) {
        this.req.updateUpsertRecord('Component_Brands_Join', '_id', row.brands[i]._id, { _id: row.brands[i]._id, priority: i + 1 })
        nodeData.process_components[rowIndex].brands[i].priority = i + 1
      }
      this.resizeNode(this.nodes_buffer[nodeIndex])
    },
    deleteNodeRowComponent: function (nodeData, rowIndex, compIndex) {
      const nodeIndex = this.nodes_buffer.findIndex((n) => n.process_spec_id === nodeData.process_spec_id)
      const row = this.nodes_buffer[nodeIndex].process_components[rowIndex]
      const comp = row.components.splice(compIndex, 1)[0]
      if (isTempKey(comp._id)) {
        this.req.removeUpsertRecord('Components_Join', '_id', comp._id)
      } else {
        this.req.deleteRecord('Components_Join', { _id: comp._id })
      }
      for (let i = compIndex; i < row.components.length; i++) {
        this.req.updateUpsertRecord('Components_Join', '_id', row.components[i]._id, { _id: row.components[i]._id, priority: i + 1 })
        nodeData.process_components[rowIndex].components[i].priority = i + 1
      }
      this.resizeNode(this.nodes_buffer[nodeIndex])
    },
    deleteNodeRow: function (nodeData, rowIndex) {
      const nodeIndex = this.nodes_buffer.findIndex((n) => n.process_spec_id === nodeData.process_spec_id)
      const row = this.nodes_buffer[nodeIndex].process_components.splice(rowIndex, 1)[0]
      row.brands.forEach(brand => {
        if (isTempKey(brand._id)) {
          this.req.removeUpsertRecord('Component_Brands_Join', '_id', brand._id)
        } else {
          this.req.deleteRecord('Component_Brands_Join', { _id: brand._id })
        }
      })
      row.components.forEach(comp => {
        if (isTempKey(comp._id)) {
          this.req.removeUpsertRecord('Components_Join', '_id', comp._id)
        } else {
          this.req.deleteRecord('Components_Join', { _id: comp._id })
        }
      })
      if (isTempKey(row.process_component_id)) {
        this.req.removeUpsertRecord('Process_Components', 'process_component_id', row.process_component_id)
      } else {
        this.req.deleteRecord('Process_Components', { process_component_id: row.process_component_id })
      }
      this.resizeNode(this.nodes_buffer[nodeIndex])
    },
    updateNodeData: function (node) {
      // update Manufacturing Process
      const updateManufacturingProcess = {
        process_spec_id: node.process_spec_id,
        product_id: node.product_id,
        current_default_process: node.current_default_process,
        process_order: node.process_order,
        special_instruction: node.special_instruction,
        manufacturing_process_id: node.manufacturing_process_id,
        custom_setup_time: node.custom_setup_time,
        custom_setup_time_units: node.custom_setup_time_units,
        custom_setup_num_employees: node.custom_setup_num_employees,
        custom_setup_time_use_default: node.custom_setup_time_use_default,
        custom_cleaning_time: node.custom_cleaning_time,
        custom_cleaning_time_units: node.custom_cleaning_time_units,
        custom_cleaning_num_employees: node.custom_cleaning_num_employees,
        custom_cleaning_time_use_default: node.custom_cleaning_time_use_default,
        manufacturing_process_version: node.manufacturing_process_version,
        position: node.position,
        type: node.type,
        variant_id: node.variant_id,
        qty_per_box: node.qty_per_box,
        box_weight_in_lbs: node.box_weight_in_lbs,
        box_sticker_required: node.box_sticker_required,
        max_pallet_layers: node.max_pallet_layers,
        boxes_per_layer: node.boxes_per_layer,
        box_id: node.box_id,
        percent_loss: node.percent_loss,
        target_process_rate: node.target_process_rate,
        target_process_rate_unit: node.target_process_rate_unit,
        target_process_rate_per: node.target_process_rate_per,
        target_process_rate_per_unit: node.target_process_rate_per_unit,
        target_process_num_employees: node.target_process_num_employees,
        primary_process: node.primary_process,
        bid_notes: node.bid_notes,
        custom_ave_percent_loss: node.custom_ave_percent_loss,
        use_default_ave_percent_loss: node.use_default_ave_percent_loss,
        num_retentions: node.num_retentions,
        lab_sample_size: node.lab_sample_size,
        qc_sample_size: node.qc_sample_size
      }
      this.req.updateUpsertRecord('Manufacturing_Process', 'process_spec_id', node.process_spec_id, updateManufacturingProcess)

      // update Process Components
      for (let i = 0; i < node.process_components.length; i++) {
        const row = node.process_components[i]
        const updateProcessComponents = {
          process_component_id: row.process_component_id,
          process_spec_id: node.process_spec_id,
          qty_per_unit: row.qty_per_unit,
          specific_brand_required: row.specific_brand_required,
          specific_component_required: row.specific_component_required
        }
        this.req.updateUpsertRecord('Process_Components', 'process_component_id', row.process_component_id, updateProcessComponents)

        // update Components Join
        for (let j = 0; j < row.components.length; j++) {
          const comp = row.components[j]
          const updateComponentsJoin = {
            _id: comp._id,
            process_component_id: row.process_component_id,
            component_id: comp.component_id,
            priority: comp.priority
          }
          this.req.updateUpsertRecord('Components_Join', '_id', comp._id, updateComponentsJoin)
        }

        // update Component Brands Join
        for (let j = 0; j < row.brands.length; j++) {
          const brand = row.brands[j]
          const updateComponentBrandsJoin = {
            _id: brand._id,
            process_component_id: row.process_component_id,
            brand_id: brand.brand_id,
            priority: brand.priority
          }
          this.req.updateUpsertRecord('Component_Brands_Join', '_id', brand._id, updateComponentBrandsJoin)
        }
      }

      const i = this.nodes_buffer.findIndex((n) => n.process_spec_id === node.process_spec_id)
      this.nodes_buffer[i] = node

      this.resizeNode(node)
    },
    resizeNode: function (node) {
      const j = this.nodes.findIndex((n) => n.data.process_spec_id === node.process_spec_id)
      if (this.instance === null) {
        return
      }
      this.instance.updateNode(this.nodes[j].id, { data: node })

      this.$nextTick(() => {
        const element = document.getElementById('my_node-' + this.nodes[j].data.process_spec_id)
        this.instance.updateNode(this.nodes[j].id, { height: element.clientHeight, width: element.clientWidth })
      })
    },
    onConnect: function (params) {
      const newEdge = {
        id: genTempKey(),
        product_id: this.productId,
        source: params.source,
        target: params.target,
        animated: false,
        marker_end: 'ArrowClosed'
      }
      this.edges_buffer.push(cloneDeep(newEdge))
      this.req.upsertRecord('Manufacturing_Process_Edges', newEdge)
      this.layoutGraph()
    },
    deleteEdge: function (edgeId) {
      const i = this.edges_buffer.findIndex((e) => String(e.id) === String(edgeId))
      if (isTempKey(edgeId)) {
        this.edges_buffer.splice(i, 1)
        this.req.removeUpsertRecord('Manufacturing_Process_Edges', 'id', edgeId)
      } else {
        this.edges_buffer.splice(i, 1)
        this.req.deleteRecord('Manufacturing_Process_Edges', { id: Number(edgeId) })
      }
      this.layoutGraph()
    },
    onEdgeUpdateEnd: function (edge) {
      const i = this.edges_buffer.findIndex((e) => e.id === edge.id)
      this.edges_buffer[i].source = edge.sourceNode?.data.process_spec_id
      this.edges_buffer[i].target = edge.targetNode?.data.process_spec_id
      this.req.updateUpsertRecord('Manufacturing_Process_Edges', 'id', edge.id, this.edges_buffer[i])
    },
    addProcess: function () {
      console.log()
      const newKey = genTempKey()
      const newProcess = {
        process_spec_id: newKey,
        product_id: this.productId,
        current_default_process: true,
        process_order: null,
        special_instruction: null,
        manufacturing_process_id: null,
        process_bid_cost: null,
        manufacturing_process_version: null,
        process_name: null,
        process_sop: null,
        rework_process: null,
        min_personnel: null,
        max_personnel: null,
        bpr_page_template: null,
        bpr_data_template: null,
        process_components: [],
        equipment: [],
        edit_manufacturing: this.edit_manufacturing,
        custom_setup_time: null,
        custom_setup_time_units: null,
        custom_setup_num_employees: null,
        custom_setup_time_use_default: true,
        custom_cleaning_time: null,
        custom_cleaning_time_units: null,
        custom_cleaning_num_employees: null,
        custom_cleaning_time_use_default: true,
        position: null,
        type: null,
        variant_id: null,
        qty_per_box: null,
        box_weight_in_lbs: null,
        box_sticker_required: null,
        max_pallet_layers: null,
        boxes_per_layer: null,
        box_id: null,
        percent_loss: null,
        target_process_rate: null,
        target_process_rate_unit: null,
        target_process_rate_per: null,
        target_process_rate_per_unit: null,
        target_process_num_employees: null,
        primary_process: true,
        bid_notes: null,
        custom_ave_percent_loss: null,
        use_default_ave_percent_loss: true,
        num_retentions: 2,
        lab_sample_size: 100,
        qc_sample_size: 5
      }
      this.nodes_buffer.push(newProcess)
      this.layoutGraph()
      this.$nextTick(() => {
        this.$nextTick(() => {
          const node = this.instance.findNode(newKey)
          this.instance.setViewport({ x: -node.position.x + 30, y: -node.position.y + 30, zoom: 1 })
        })
      })
    },
    deleteProcess: function (node) {
      const i = this.nodes_buffer.findIndex((n) => n.process_spec_id === node.process_spec_id)
      for (let j = 0; j < node.process_components.length; j++) {
        this.deleteNodeRow(node, j)
      }
      this.nodes_buffer.splice(i, 1)
      const deleteEdges = []
      for (let k = 0; k < this.edges_buffer.length; k++) {
        if (this.edges_buffer[k].source === node.process_spec_id || this.edges_buffer[k].target === node.process_spec_id) {
          deleteEdges.push(this.edges_buffer[k].id)
        }
      }
      for (let p = 0; p < deleteEdges.length; p++) {
        this.deleteEdge(deleteEdges[p])
        this.edges_buffer.splice(this.edges_buffer.findIndex((e) => e.id === deleteEdges[p]), 1)
      }
      if (isTempKey(node.process_spec_id)) {
        this.req.removeUpsertRecord('Manufacturing_Process', 'process_spec_id', node.process_spec_id)
      } else {
        this.req.deleteRecord('Manufacturing_Process', { process_spec_id: node.process_spec_id })
      }
      this.layoutGraph()
    },
    setProcessesBuffer: function () {
      this.toggleEditProcesses()
      this.$nextTick(() => {
        this.layoutGraph()
      })
    },
    cancel: function () {
      this.req = new CustomRequest(this.$cookies.get('session'))
      this.$emit('toggleLoaded', false)
      this.$emit('refreshParent')
    },
    submit: async function () {
      // Check valid formula
      this.$emit('toggleLoaded', false)
      if (!this.validateManufacturing()) {
        this.$emit('toggleLoaded', true)
        return
      }

      const resp = await this.req.sendRequest(window.origin)

      const createToast = this.$root.createToast
      resp.messages.flash.forEach(message => {
        createToast(message)
      })

      if (resp.status === 201) {
        this.edit_manufacturing = false
        this.$parent.edit_manufacturing = false
        this.$parent.getProductData()
      } else {
        this.edit_manufacturing = false
        this.$parent.edit_manufacturing = false
        this.$nextTick(() => {
          this.$parent.toggleLoaded(true)
        })
      }
    },
    validateManufacturing: function () {
      this.$bvToast.hide()
      const createToast = this.$root.createToast
      const errorToast = {
        title: 'Invalid Process',
        message: '',
        variant: 'warning',
        visible: true,
        no_close_button: false,
        no_auto_hide: true,
        auto_hide_delay: false
      }

      let flag = true
      for (let i = 0; i < this.nodes_buffer.length; i++) {
        if (this.nodes_buffer[i].process_name === null || this.nodes_buffer[i].process_name === '') {
          errorToast.message = 'Process Name is required.'
          createToast(errorToast)
          return false
        }
        errorToast.title = `${this.nodes_buffer[i].process_name} is invalid.`
        if (!this.validateNode(this.nodes_buffer[i], createToast, errorToast)) {
          flag = false
        }
      }
      return flag
    },
    validateNode: function (node, createToast, errorToast) {
      let flag = true
      if (node.requires_product_variant && (node.variant_id === null || node.variant_id === '')) {
        errorToast.message = 'Variant is required.'
        createToast(errorToast)
        flag = false
      }
      if (!this.validateNodePercent(node, createToast, errorToast)) {
        flag = false
      }
      if (!this.validateNodeLeanManufacturing(node, createToast, errorToast)) {
        flag = false
      }
      if (node.requires_components) {
        for (let i = 0; i < node.process_components.length; i++) {
          if (!this.validateNodeComponent(node.process_components[i], createToast, errorToast)) {
            errorToast.message = `${node.process_name} has invalid components.`
            createToast(errorToast)
            flag = false
          }
        }
      }
      if (node.requires_box_specs && !this.validateNodePalletization(node, createToast, errorToast)) {
        flag = false
      }
      if (node.requires_samples && !this.validateNodeSamples(node, createToast, errorToast)) {
        flag = false
      }
      if (node.requires_retention && !this.validateNodeRetention(node, createToast, errorToast)) {
        flag = false
      }
      return flag
    },
    validateNodePercent: function (node, createToast, errorToast) {
      let flag = true
      if (node.custom_percent_ave_loss === null || node.custom_percent_ave_loss === '') {
        errorToast.message = 'Percent Loss is required.'
        createToast(errorToast)
        flag = false
      }
      if (node.custom_percent_ave_loss <= 0 || node.custom_percent_ave_loss > 100) {
        errorToast.message = 'Percent Loss must be between 0 and 100.'
        createToast(errorToast)
        flag = false
      }
      return flag
    },
    validateNodeLeanManufacturing: function (node, createToast, errorToast) {
      let flag = true
      // Setup Validation
      if (node.custom_setup_time_use_default === false) {
        if (node.custom_setup_time === null || node.custom_setup_time === '') {
          errorToast.message = 'Custom Setup Time is required.'
          createToast(errorToast)
          flag = false
        }
        if (node.custom_setup_time < 0) {
          errorToast.message = 'Custom Setup Time must be greater than or equal to 0.'
          createToast(errorToast)
          flag = false
        }
        if (node.custom_setup_time_units === null || node.custom_setup_time_units === '') {
          errorToast.message = 'Custom Setup Time Units is required.'
          createToast(errorToast)
          flag = false
        }
        if (node.custom_setup_num_employees === null || node.custom_setup_num_employees === '') {
          errorToast.message = 'Custom Setup Number of Employees is required.'
          createToast(errorToast)
          flag = false
        }
        if (node.custom_setup_num_employees < 0) {
          errorToast.message = 'Custom Setup Number of Employees must be greater than or equal to 0.'
          createToast(errorToast)
          flag = false
        }
      }

      // Processing Rate Validation
      if (node.target_process_rate === null || node.target_process_rate === '') {
        errorToast.message = 'Target Process Rate is required.'
        createToast(errorToast)
        flag = false
      }
      if (node.target_process_rate < 0) {
        errorToast.message = 'Target Process Rate must be greater than or equal to 0.'
        createToast(errorToast)
        flag = false
      }
      if (node.target_process_rate_per === null || node.target_process_rate_per === '') {
        errorToast.message = 'Target Process Rate Per is required.'
        createToast(errorToast)
        flag = false
      }
      if (node.target_process_rate_per < 0) {
        errorToast.message = 'Target Process Rate Per must be greater than or equal to 0.'
        createToast(errorToast)
        flag = false
      }
      if (node.target_process_rate_per_unit === null || node.target_process_rate_per_unit === '') {
        errorToast.message = 'Target Process Rate Per Unit is required.'
        createToast(errorToast)
        flag = false
      }
      if (node.target_process_num_employees === null || node.target_process_num_employees === '') {
        errorToast.message = 'Target Process Number of Employees is required.'
        createToast(errorToast)
        flag = false
      }
      if (node.target_process_num_employees < 0) {
        errorToast.message = 'Target Process Number of Employees must be greater than or equal to 0.'
        createToast(errorToast)
        flag = false
      }

      // Cleaning Validation
      if (node.custom_cleaning_time_use_default === false) {
        if (node.custom_cleaning_time === null || node.custom_cleaning_time === '') {
          errorToast.message = 'Custom Cleaning Time is required.'
          createToast(errorToast)
          flag = false
        }
        if (node.custom_cleaning_time < 0) {
          errorToast.message = 'Custom Cleaning Time must be greater than or equal to 0.'
          createToast(errorToast)
          flag = false
        }
        if (node.custom_cleaning_time_units === null || node.custom_cleaning_time_units === '') {
          errorToast.message = 'Custom Cleaning Time Units is required.'
          createToast(errorToast)
          flag = false
        }
        if (node.custom_cleaning_num_employees === null || node.custom_cleaning_num_employees === '') {
          errorToast.message = 'Custom Cleaning Number of Employees is required.'
          createToast(errorToast)
          flag = false
        }
        if (node.custom_cleaning_num_employees < 0) {
          errorToast.message = 'Custom Cleaning Number of Employees must be greater than or equal to 0.'
          createToast(errorToast)
          flag = false
        }
      }
      return flag
    },
    validateNodeSamples: function (node, createToast, errorToast) {
      let flag = true
      // Check Component Count
      if (node.lab_sample_size === null || node.lab_sample_size === '') {
        errorToast.message = 'Lab Sample Size is required.'
        createToast(errorToast)
        flag = false
      }
      if (node.lab_sample_size < 0) {
        errorToast.message = 'Lab Sample Size must be greater than or equal to 0.'
        createToast(errorToast)
        flag = false
      }
      if (node.qc_sample_size === null || node.qc_sample_size === '') {
        errorToast.message = 'QC Sample Size is required.'
        createToast(errorToast)
        flag = false
      }
      if (node.qc_sample_size < 0) {
        errorToast.message = 'QC Sample Size must be greater than or equal to 0.'
        createToast(errorToast)
        flag = false
      }
      return flag
    },
    validateNodeRetention: function (node, createToast, errorToast) {
      let flag = true
      // Check Component Count
      if (node.num_retentions === null || node.num_retentions === '') {
        errorToast.message = 'Retention Count is required.'
        createToast(errorToast)
        flag = false
      }
      if (node.num_retentions < 0) {
        errorToast.message = 'Retention Count must be greater than or equal to 0.'
        createToast(errorToast)
        flag = false
      }
      return flag
    },
    validateNodeComponent: function (processComponentRow, createToast, errorToast) {
      let flag = true
      // Check Component Count
      if (processComponentRow.qty_per_unit === null || processComponentRow.qty_per_unit === '') {
        errorToast.message = 'Quantity per Unit is required.'
        createToast(errorToast)
        flag = false
      }
      if (processComponentRow.qty_per_unit <= 0) {
        errorToast.message = 'Quantity per Unit must be greater than 0.'
        createToast(errorToast)
        flag = false
      }

      // Check valid Components
      for (let i = 0; i < processComponentRow.components.length; i++) {
        if (!processComponentRow.components[i].component_id > 0) {
          errorToast.message = 'Invalid components selected.'
          createToast(errorToast)
          flag = false
        }
      }

      // Check valid Brands
      for (let i = 0; i < processComponentRow.brands.length; i++) {
        if (!processComponentRow.brands[i].brand_id > 0) {
          errorToast.message = 'Invalid brands selected.'
          createToast(errorToast)
          flag = false
        }
      }
      return flag
    },
    validateNodePalletization: function (node, createToast, errorToast) {
      let flag = true
      if (node.qty_per_box === null || node.qty_per_box === '') {
        errorToast.message = 'Quantity per Box is required.'
        createToast(errorToast)
        flag = false
      }
      if (node.qty_per_box <= 0) {
        errorToast.message = 'Quantity per Box must be greater than 0.'
        createToast(errorToast)
        flag = false
      }
      // if (node.box_weight_in_lbs === null || node.box_weight_in_lbs === '') {
      //   errorToast.message = 'Box Weight in lbs is required.'
      //   createToast(errorToast)
      //   flag = false
      // }
      if (node.box_weight_in_lbs <= 0) {
        errorToast.message = 'Box Weight in lbs must be greater than 0.'
        createToast(errorToast)
        flag = false
      }
      if (node.max_pallet_layers === null || node.max_pallet_layers === '') {
        errorToast.message = 'Max Pallet Layers is required.'
        createToast(errorToast)
        flag = false
      }
      if (node.max_pallet_layers <= 0) {
        errorToast.message = 'Max Pallet Layers must be greater than 0.'
        createToast(errorToast)
        flag = false
      }
      if (node.boxes_per_layer === null || node.boxes_per_layer === '') {
        errorToast.message = 'Boxes per Layer is required.'
        createToast(errorToast)
        flag = false
      }
      if (node.boxes_per_layer <= 0) {
        errorToast.message = 'Boxes per Layer must be greater than 0.'
        createToast(errorToast)
        flag = false
      }
      if (node.box_id === null || node.box_id === '') {
        errorToast.message = 'Box is required.'
        createToast(errorToast)
        flag = false
      }
      return flag
    },
    toggleEditProcesses: function () {
      this.edit_manufacturing = !this.edit_manufacturing
      this.$emit('edit-manufacturing', this.edit_manufacturing)
    },
    onPaneReady: function (vueFlowInstance) {
      this.instance = vueFlowInstance
      this.layoutGraph()
      this.$nextTick(() => {
        this.zoomfit()
      })
    },
    zoomin: function () {
      this.instance.zoomIn()
    },
    zoomout: function () {
      this.instance.zoomOut()
    },
    zoomfit: function () {
      if (this.nodes.length > 0) {
        this.instance.setViewport({ x: this.nodes[0].position.x / 2, y: 0, zoom: 0.2 })
      }
    },
    renderGraph: function () {
      this.nodes = []
      this.edges = []
      this.loading = true

      // build Nodes
      for (let i = 0; i < this.nodes_buffer.length; i++) {
        const data = this.nodes_buffer[i]
        const node = {
          id: data.process_spec_id.toString(),
          label: data.process_name,
          position: { x: 0, y: 0 },
          data: data,
          type: 'manufacturing-process',
          toolbarVisible: false
        }
        // Render Node
        this.nodes.push(node)
      }

      // build Edges
      for (let i = 0; i < this.edges_buffer.length; i++) {
        const edge = {
          id: this.edges_buffer[i].id,
          source: typeof this.edges_buffer[i].source !== 'string' ? this.edges_buffer[i].source.toString() : this.edges_buffer[i].source,
          target: typeof this.edges_buffer[i].target !== 'string' ? this.edges_buffer[i].target.toString() : this.edges_buffer[i].target,
          animated: this.edges_buffer[i].animated,
          updatable: this.edit_manufacturing,
          type: 'button',
          markerEnd: MarkerType.ArrowClosed
        }
        if (edge.source === edge.target) {
          continue
        }
        // Render Edges
        this.edges.push(edge)
      }
    },
    layoutGraph: async function () {
      // Create a new directed graph
      var g = new dagre.graphlib.Graph({ directed: true })

      // Set an object for the graph label
      g.setGraph({})

      // Default to assigning a new object as a label for each new edge.
      g.setDefaultEdgeLabel(function () { return {} })

      this.renderGraph()

      await this.$nextTick() // Wait for nodes to render before setting their dimensions

      // Input Nodes
      let maxWidth = 0
      let maxHeight = 0
      for (let i = 0; i < this.nodes.length; i++) {
        const node = this.nodes[i]
        const graphNode = this.instance.findNode(node.id)
        if (maxWidth < graphNode.dimensions.width) {
          maxWidth = graphNode.dimensions.width
        }
        if (maxHeight < graphNode.dimensions.height) {
          maxHeight = graphNode.dimensions.height
        }
      }

      for (let i = 0; i < this.nodes.length; i++) {
        g.setNode(this.nodes[i].id, { width: maxWidth + 30, height: maxHeight + 80 })
      }

      // Input Edges
      for (let i = 0; i < this.edges.length; i++) {
        g.setEdge(this.edges[i].source, this.edges[i].target)
      }

      // Calculate the layout (i.e. node positions)
      dagre.layout(g)

      for (let i = 0; i < this.nodes.length; i++) {
        const node = this.nodes[i]
        const nodeWithPosition = g.node(node.id)
        this.nodes[i].position = { x: nodeWithPosition.x, y: nodeWithPosition.y }
      }

      this.loading = false
    },
    get_brands: function () {
      const fetchRequest = window.origin + '/api/v1/organizations'
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
            const orgs = Object.values(data.data)
            this.brand_options = orgs.sort((a, b) => {
              return a?.organization_primary_name > b?.organization_primary_name ? 1 : -1
            })
            // eslint-disable-next-line
            console.log(this.brand_options)
            if (this.brand_options.doc === null) {
              this.brand_options.doc = {}
            }
          })
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
    get_components: function () {
      const fetchRequest = window.origin + '/api/v1/catalogue/components?type=container&type=pouch&type=shrink_band&type=lid&type=label&type=capsule&type=misc&type=scoop&type=desiccant&type=box&type=carton&type=packaging_material'
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
            const ings = Object.values(data.data)
            this.component_options = ings.sort((a, b) => (a.component_primary_name > b.component_name ? 1 : -1))
            // eslint-disable-next-line
            console.log(this.component_options)
          })
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
    get_processes: function () {
      const fetchRequest = window.origin + '/api/v1/processes?populate=equipment'
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
            const ings = Object.values(data.data)
            this.process_options = ings.sort((a, b) => (a.component_primary_name > b.component_name ? 1 : -1))
            // eslint-disable-next-line
            console.log(this.process_options)
          })
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
    }
  },
  created: function () {
    this.nodes_buffer = cloneDeep(this.manufacturing.nodes)
    this.edges_buffer = cloneDeep(this.manufacturing.edges)
    this.renderGraph()
    this.get_brands()
    this.get_components()
    this.get_processes()
  }
}
</script>

<style scoped>
@import '@vue-flow/core/dist/theme-default.css';
@import '@vue-flow/core/dist/style.css';
@import '@vue-flow/core/dist/style.css';
@import '@vue-flow/controls/dist/style.css';
@import '@vue-flow/minimap/dist/style.css';
@import '@vue-flow/node-resizer/dist/style.css';
@import '../../../assets/vue-flow-css/index.css';

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

<style>
.vue-flow__edge-path {
  stroke-width: 16;
}
</style>

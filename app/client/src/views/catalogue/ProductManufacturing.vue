<template>
  <div>
    <h3 id="Manufacturing">Manufacturing<b-button v-if="!edit_manufacturing" v-b-tooltip.hover title="Edit Manufacturing Process" v-on:click="edit_manufacturing = !edit_manufacturing" class="btn p-1 ml-2 btn-light" type="button"><b-icon icon="pencil-square" class="d-print-none"></b-icon></b-button></h3>
    <div class="my_component d-flex flex-wrap justify-content-center">
      <div class="d-flex justify-content-center" style="width: 100%; height: 700px">
        <VueFlow @pane-ready="onPaneReady" class="vue-flow-basic-example" :nodes="nodes" :edges="edges" :nodesConnectable="false" :nodesDraggable="false" :max-zoom="2" :min-zoom="0.3" :zoom-on-double-click="true" :no-wheel-class-name="false" :prevent-scrolling="false">
          <Background />
          <Panel position="top-right">
            <b-button-group>
              <b-button variant="light" style="border-width: 1px; border-color:#999999" @click="zoomin()"><b-icon icon="zoom-in"></b-icon></b-button>
              <b-button variant="light" style="border-width: 1px; border-color:#999999" @click="zoomout()"><b-icon icon="zoom-out"></b-icon></b-button>
              <b-button variant="light" style="border-width: 1px; border-color:#999999" @click="zoomfit()"><b-icon icon="fullscreen"></b-icon></b-button>
            </b-button-group>
          </Panel>
          <Panel position="bottom-left">
            <b-button variant="light" style="border-width: 1px; border-color:#999999">New Process</b-button>
          </Panel>
          <MiniMap />
          <template #node-manufacturing-process="node_data">
            <ManufacturingProcess :id="node_data.id" :node_data="node_data" />
          </template>
        </VueFlow>
      </div>
    </div>
  </div>
</template>

<script>
import dagre from '@dagrejs/dagre'
import { Panel, VueFlow } from '@vue-flow/core'
import { Background } from '@vue-flow/background'
import { MiniMap } from '@vue-flow/minimap'
import ManufacturingProcess from './ManufacturingProcess.vue'

export default {
  name: 'ProductManufacturing',
  components: {
    VueFlow,
    MiniMap,
    Background,
    Panel,
    ManufacturingProcess
  },
  props: {
    manufacturing: {
      type: Object,
      required: true
    },
    edit: {
      type: Boolean,
      required: true,
      default: false
    }
  },
  data: function () {
    return {
      nodes: [],
      edges: [],
      edit_manufacturing: this.edit
    }
  },
  methods: {
    onPaneReady: function (vueFlowInstance) {
      this.instance = vueFlowInstance
      this.instance.fitView()
    },
    zoomin: function () {
      this.instance.zoomIn()
    },
    zoomout: function () {
      this.instance.zoomOut()
    },
    zoomfit: function () {
      this.instance.fitView()
    }
  },
  created: function () {
    // Create a new directed graph
    var g = new dagre.graphlib.Graph()

    // Set an object for the graph label
    g.setGraph({})

    // Default to assigning a new object as a label for each new edge.
    g.setDefaultEdgeLabel(function () { return {} })

    function calcHeight (node) {
      let height = 260
      height += node.components.length > 0 ? 50 : 0
      height += node.components.length * 140
      for (let i = 0; node.components.length > i; i++) {
        const subrow = Math.max(
          node.components[i]?.components.length || 1,
          node.components[i]?.brands.length || 0
        )
        height += (subrow - 1) * 140
      }
      return height
    }

    // build Nodes
    const nodes = []
    for (let i = 0; i < this.manufacturing.nodes.length; i++) {
      const node = {
        id: this.manufacturing.nodes[i].process_spec_id.toString(),
        label: this.manufacturing.nodes[i].process_name,
        position: { x: 0, y: 0 },
        data: this.manufacturing.nodes[i],
        type: 'manufacturing-process',
        width: this.manufacturing.nodes[i].components.length > 0 ? 1200 : 600,
        height: calcHeight(this.manufacturing.nodes[i]),
        toolbarVisible: false
      }
      nodes.push(node)
      g.setNode(node.id, { height: node.height + 200, width: node.width })
    }

    // build Edges
    const edges = []
    for (let i = 0; i < this.manufacturing.edges.length; i++) {
      const edge = {
        id: this.manufacturing.edges[i].id,
        source: this.manufacturing.edges[i].source.toString(),
        target: this.manufacturing.edges[i].target.toString(),
        animated: this.manufacturing.edges[i].animated,
        type: 'smoothstep'
      }
      if (edge.source === edge.target) {
        continue
      }
      edges.push(edge)
      g.setEdge(edge.source, edge.target)
    }

    // Calculate the layout (i.e. node positions)
    dagre.layout(g)
    g.nodes().forEach(function (v) {
      const position = { x: g.node(v).x, y: g.node(v).y }
      for (let i = 0; i < nodes.length; i++) {
        if (nodes[i].id === v) {
          nodes[i].position = position
          break
        }
      }
    })
    this.nodes = nodes
    this.edges = edges
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
@import '../../assets/vue-flow-css/index.css';

.vue-flow__minimap {
  transform: scale(75%);
  transform-origin: bottom right;
}

.basicflow.dark {
  background: #000000;
  color: #fffffb
}

.basicflow.dark .vue-flow__node {
  background: hsl(0, 0%, 10%);
  color: #fffffb
}

.basicflow.dark .vue-flow__node.selected {
  background: hsl(0, 0%, 20%);
  border: 1px solid hotpink
}

.basicflow .vue-flow__controls {
  display: flex;
  flex-wrap: wrap;
  justify-content: center
}

.basicflow.dark .vue-flow__controls {
  border: 1px solid #FFFFFB
}

.basicflow .vue-flow__controls .vue-flow__controls-button {
  border: none;
  border-right: 1px solid #eee
}

.basicflow.dark .vue-flow__controls .vue-flow__controls-button {
  background: hsl(0, 0%, 20%);
  fill: #fffffb;
  border: none
}

.basicflow.dark .vue-flow__controls .vue-flow__controls-button:hover {
  background: hsl(0, 0%, 30%)
}

.basicflow.dark .vue-flow__edge-textbg {
  fill: #292524
}

.basicflow.dark .vue-flow__edge-text {
  fill: #fffffb
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

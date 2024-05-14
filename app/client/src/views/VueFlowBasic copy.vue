<script setup>
import { ref } from 'vue'
import { VueFlow, useVueFlow, MarkerType } from '@vue-flow/core'
import { Background } from '@vue-flow/background'
import { ControlButton, Controls } from '@vue-flow/controls'
import { MiniMap } from '@vue-flow/minimap'
import VueFlowIcon from './VueFlowIcon.vue'

const initialNodes = [
  { id: '1', type: 'input', label: 'Node 1', position: { x: 250, y: 0 }, class: 'light' },
  { id: '2', type: 'output', label: 'Node 2', position: { x: 100, y: 100 }, class: 'light' },
  { id: '3', label: 'Node 3', position: { x: 400, y: 100 }, class: 'light' },
  { id: '4', label: 'Node 4', position: { x: 150, y: 200 }, class: 'light' },
  { id: '5', type: 'output', label: 'Node 5', position: { x: 300, y: 300 }, class: 'light' }
]

const initialEdges = [
  { id: 'e1-2', source: '1', target: '2', animated: true },
  { id: 'e1-3', label: 'edge with arrowhead', source: '1', target: '3', markerEnd: MarkerType.ArrowClosed },
  {
    id: 'e4-5',
    type: 'step',
    label: 'step-edge',
    source: '4',
    target: '5',
    style: { stroke: 'orange' },
    labelBgStyle: { fill: 'orange' }
  },
  { id: 'e3-4', type: 'smoothstep', label: 'smoothstep-edge', source: '3', target: '4' }
]

/**
 * useVueFlow provides all event handlers and store properties
 * You can pass the composable an object that has the same properties as the VueFlow component props
 */
const { onPaneReady, onNodeDragStop, onConnect, addEdges, setViewport, toObject } = useVueFlow()

const nodes = ref(initialNodes)

const edges = ref(initialEdges)

// our dark mode toggle flag
const dark = ref(true)

/**
 * This is a Vue Flow event-hook which can be listened to from anywhere you call the composable, instead of only on the main component
 * Any event that is available as `@event-name` on the VueFlow component is also available as `onEventName` on the composable and vice versa
 *
 * onPaneReady is called when viewpane & nodes have visible dimensions
 */
onPaneReady(({ fitView }) => {
  fitView()
})

/**
 * onNodeDragStop is called when a node is done being dragged
 *
 * Node drag events provide you with:
 * 1. the event object
 * 2. the nodes array (if multiple nodes are dragged)
 * 3. the node that initiated the drag
 * 4. any intersections with other nodes
 */
onNodeDragStop(({ event, nodes, node, intersections }) => {
  console.log('Node Drag Stop', { event, nodes, node, intersections })
})

/**
 * onConnect is called when a new connection is created.
 *
 * You can add additional properties to your new edge (like a type or label) or block the creation altogether by not calling `addEdges`
 */
onConnect((connection) => {
  addEdges(connection)
})

/**
 * To update a node or multiple nodes, you can
 * 1. Mutate the node objects *if* you're using `v-model`
 * 2. Use the `updateNode` method (from `useVueFlow`) to update the node(s)
 * 3. Create a new array of nodes and pass it to the `nodes` ref
 */
function updatePos () {
  nodes.value = nodes.value.map((node) => {
    return {
      ...node,
      position: {
        x: Math.random() * 400,
        y: Math.random() * 400
      }
    }
  })
}

/**
 * toObject transforms your current graph data to an easily persist-able object
 */
function logToObject () {
  console.log(toObject())
}

/**
 * Resets the current viewport transformation (zoom & pan)
 */
function resetTransform () {
  setViewport({ x: 0, y: 0, zoom: 1 })
}

function toggleDarkMode () {
  dark.value = !dark.value
}
</script>

<style scoped>
@import '@vue-flow/core/dist/theme-default.css';
@import '@vue-flow/core/dist/style.css';
@import '../assets/vue-flow-css/index.css';
@import 'https://cdn.jsdelivr.net/npm/@vue-flow/core@1.33.6/dist/style.css';
@import 'https://cdn.jsdelivr.net/npm/@vue-flow/core@1.33.6/dist/theme-default.css';
@import 'https://cdn.jsdelivr.net/npm/@vue-flow/controls@latest/dist/style.css';
@import 'https://cdn.jsdelivr.net/npm/@vue-flow/minimap@latest/dist/style.css';
@import 'https://cdn.jsdelivr.net/npm/@vue-flow/node-resizer@latest/dist/style.css';
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

<template>
  <div class="my_component d-flex flex-wrap justify-content-center">
    <div class="card my-2" v-show="!loaded">
      <div class="card-body">
        <div class="d-flex justify-content-center" style="width: 1200px;height: 800px">
          <VueFlow :nodes="nodes" :edges="edges" :class="{ dark }" class="basicflow" :default-viewport="{ zoom: 1.5 }" :min-zoom="0.2" :max-zoom="4">
            <Background pattern-color="#aaa" :gap="16" />

            <MiniMap />

            <Controls position="top-right">
              <ControlButton title="Reset Transform" @click="resetTransform">
                <VueFlowIcon name="reset" />
              </ControlButton>

              <ControlButton title="Shuffle Node Positions" @click="updatePos">
                <VueFlowIcon name="update" />
              </ControlButton>

              <ControlButton title="Toggle Dark Mode" @click="toggleDarkMode">
                <VueFlowIcon v-if="dark" name="sun" />
                <VueFlowIcon v-else name="moon" />
              </ControlButton>

              <ControlButton title="Log `toObject`" @click="logToObject">
                <VueFlowIcon name="log" />
              </ControlButton>
            </Controls>
          </VueFlow>
        </div>
      </div>
    </div>
  </div>
</template>






<template>
  <div class="my_component d-flex flex-wrap justify-content-center">
    <div class="card my-2" v-show="!loaded">
      <div class="card-body">
        <div class="d-flex justify-content-center" style="width: 1200px;height: 800px">
          <VueFlow :nodes="nodes" :edges="edges" :class="{ dark }" class="basicflow" :default-viewport="{ zoom: 1.5 }" :min-zoom="0.2" :max-zoom="4">
            <Background pattern-color="#aaa" :gap="16" />

            <MiniMap />

            <Controls position="top-right">
              <ControlButton title="Reset Transform" @click="resetTransform()">
                <VueFlowIcon name="reset" />
              </ControlButton>

              <ControlButton title="Shuffle Node Positions" @click="updatePos()">
                <VueFlowIcon name="update" />
              </ControlButton>

              <ControlButton title="Toggle Dark Mode" @click="toggleDarkMode()">
                <VueFlowIcon v-if="dark" name="sun" />
                <VueFlowIcon v-else name="moon" />
              </ControlButton>

              <ControlButton title="Log `toObject`" @click="logToObject()">
                <VueFlowIcon name="log" />
              </ControlButton>
            </Controls>
          </VueFlow>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import '@vue-flow/core/dist/theme-default.css';
@import '@vue-flow/core/dist/style.css';
@import '../assets/vue-flow-css/index.css';
@import 'https://cdn.jsdelivr.net/npm/@vue-flow/core@1.33.6/dist/style.css';
@import 'https://cdn.jsdelivr.net/npm/@vue-flow/core@1.33.6/dist/theme-default.css';
@import 'https://cdn.jsdelivr.net/npm/@vue-flow/controls@latest/dist/style.css';
@import 'https://cdn.jsdelivr.net/npm/@vue-flow/minimap@latest/dist/style.css';
@import 'https://cdn.jsdelivr.net/npm/@vue-flow/node-resizer@latest/dist/style.css';

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

<script>
import { VueFlow, useVueFlow, MarkerType } from '@vue-flow/core'
import { Background } from '@vue-flow/background'
import { ControlButton, Controls } from '@vue-flow/controls'
import { MiniMap } from '@vue-flow/minimap'
import VueFlowIcon from './VueFlowIcon.vue'

/**
 * useVueFlow provides all event handlers and store properties
 * You can pass the composable an object that has the same properties as the VueFlow component props
 */
const { onPaneReady, onNodeDragStop, onConnect, addEdges, setViewport, toObject } = useVueFlow()

export default {
  components: {
    VueFlow,
    Background,
    ControlButton,
    Controls,
    MiniMap,
    VueFlowIcon
  },
  data: function () {
    return {
      nodes: [
        { id: '1', type: 'input', label: 'Node 1', position: { x: 250, y: 0 }, class: 'light' },
        { id: '2', type: 'output', label: 'Node 2', position: { x: 100, y: 100 }, class: 'light' },
        { id: '3', label: 'Node 3', position: { x: 400, y: 100 }, class: 'light' },
        { id: '4', label: 'Node 4', position: { x: 150, y: 200 }, class: 'light' },
        { id: '5', type: 'output', label: 'Node 5', position: { x: 300, y: 300 }, class: 'light' }
      ],
      edges: [
        { id: 'e1-2', source: '1', target: '2', animated: true },
        { id: 'e1-3', label: 'edge with arrowhead', source: '1', target: '3', markerEnd: MarkerType.ArrowClosed },
        {
          id: 'e4-5',
          type: 'step',
          label: 'step-edge',
          source: '4',
          target: '5',
          style: { stroke: 'orange' },
          labelBgStyle: { fill: 'orange' }
        },
        { id: 'e3-4', type: 'smoothstep', label: 'smoothstep-edge', source: '3', target: '4' }
      ],
      dark: false
    }
  },
  methods: {
    /**
     * This is a Vue Flow event-hook which can be listened to from anywhere you call the composable, instead of only on the main component
     * Any event that is available as `@event-name` on the VueFlow component is also available as `onEventName` on the composable and vice versa
     *
     * onPaneReady is called when viewpane & nodes have visible dimensions
     */
    onPaneReady: onPaneReady(({ fitView }) => {
      fitView()
    }),
    /**
     * onNodeDragStop is called when a node is done being dragged
     *
     * Node drag events provide you with:
     * 1. the event object
     * 2. the nodes array (if multiple nodes are dragged)
     * 3. the node that initiated the drag
     * 4. any intersections with other nodes
     */
    onNodeDragStop: onNodeDragStop(({ event, nodes, node, intersections }) => {
      console.log('Node Drag Stop', { event, nodes, node, intersections })
    }),
    /**
     * onConnect is called when a new connection is created.
     *
     * You can add additional properties to your new edge (like a type or label) or block the creation altogether by not calling `addEdges`
     */
    onConnect: onConnect((connection) => {
      addEdges(connection)
    }),
    /**
     * To update a node or multiple nodes, you can
     * 1. Mutate the node objects *if* you're using `v-model`
     * 2. Use the `updateNode` method (from `useVueFlow`) to update the node(s)
     * 3. Create a new array of nodes and pass it to the `nodes` ref
     */
    updatePos: function () {
      this.nodes.value = this.nodes.value.map((node) => {
        return {
          ...node,
          position: {
            x: Math.random() * 400,
            y: Math.random() * 400
          }
        }
      })
    },
    /**
     * toObject transforms your current graph data to an easily persist-able object
     */
    logToObject: function () {
      console.log(toObject())
    },
    /**
     * Resets the current viewport transformation (zoom & pan)
     */
    resetTransform: function () {
      setViewport({ x: 0, y: 0, zoom: 1 })
    },
    toggleDarkMode: function () {
      this.dark.value = !this.dark.value
    }
  }
}
</script>

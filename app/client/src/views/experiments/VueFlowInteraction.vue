<script setup>
import { ref } from 'vue'
import { VueFlow, MarkerType } from '@vue-flow/core'
import InteractionControls from './InteractionControls.vue'

const nodes = ref([
  { id: '1', type: 'input', label: 'Node 1', position: { x: 250, y: 5 } },
  { id: '2', label: 'Node 2', position: { x: 100, y: 100 } },
  { id: '3', label: 'Node 3', position: { x: 400, y: 100 } },
  { id: '4', label: 'Node 4', position: { x: 400, y: 200 } }
])

const edges = ref([
  { id: 'e1-2', source: '1', target: '2', animated: true },
  { id: 'e1-3', source: '1', target: '3', markerEnd: MarkerType.ArrowClosed }
])
</script>

<style scoped>
@import '@vue-flow/core/dist/theme-default.css';
@import '@vue-flow/core/dist/style.css';
@import '../assets/vue-flow-css/index.css';

.interactionflow .controls {
  position: absolute;
  left: 0;
  top: 0;
  z-index: 4;
  font-size: 11px;
  background-color: #d3d3d3;
  border-bottom-right-radius: 10px;
  padding: 8px
}

.interactionflow .controls .label {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 5px;
  cursor: pointer
}

.interactionflow .controls .label input {
  cursor: pointer
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
    <!-- <div class="card my-2">
      <div class="card-body">
        <div class="d-flex justify-content-center">
          <div class="spinner-border text-primary" role="status"></div>
        </div>
      </div>
    </div> -->
    <div class="card my-2">
      <div class="card-body">
        <div class="d-flex justify-content-center" style="width: 1200px;height: 800px">

          <VueFlow :nodes="nodes" :edges="edges" class="interactionflow" fit-view-on-init>
            <InteractionControls />
          </VueFlow>
        </div>
      </div>
    </div>
  </div>
</template>

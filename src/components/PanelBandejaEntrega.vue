<template>
  <q-splitter v-model="splitterModel" style="height: 500px">
    <template v-slot:before>
      <q-tabs
        no-caps
        v-model="innerTab"
        vertical
        class="tablaAcciones q-pa-sm"
        active-color="primary"
        indicator-color="primary"
      >
        <q-tab name="borrador">
          <q-avatar
            size="md"
            color="cyan-10"
            text-color="white"
            icon="drive_file_rename_outline"
          />
          Borrador ({{ entregas.borradores.length }})
        </q-tab>
        <q-tab name="enviadoLider">
          <q-avatar
            size="md"
            color="cyan-10"
            text-color="white"
            icon="supervisor_account"
          />
          Enviado a líder ({{ entregas.enviados_Lider.length }})
        </q-tab>
        <q-tab name="rechazadoLider">
          <q-avatar
            size="md"
            color="cyan-10"
            text-color="white"
            icon="warning"
          />
          Rechazado (líder) ({{ entregas.rechazados_Lider.length }})
        </q-tab>
        <q-tab name="enviadoUPCI">
          <q-avatar size="md" color="cyan-10" text-color="white" icon="woman" />
          Enviado a UPCI ({{ entregas.enviados_UPCI.length }})
        </q-tab>
        <q-tab name="rechazadoUPCI">
          <q-avatar size="md" color="cyan-10" text-color="white" icon="error" />
          Rechazado (UPCI) ({{ entregas.rechazados_UPCI.length }})
        </q-tab>
        <q-tab name="finalizado">
          <q-avatar
            size="md"
            color="cyan-10"
            text-color="white"
            icon="self_improvement"
          />
          Finalizado ({{ entregas.finalizados.length }})
        </q-tab>
      </q-tabs>
    </template>
    <template v-slot:after>
      <q-tab-panels
        v-model="innerTab"
        animated
        transition-prev="slide-down"
        transition-next="slide-up"
        class="tablaAcciones"
      >
        <q-tab-panel name="borrador">
          <TablaEntregasColaborador
            :entregas="entregas.borradores"
            :usuario="usuario"
            :tipoEntrega="tipoEntrega"
          />
        </q-tab-panel>
        <q-tab-panel name="enviadoLider">
          <TablaEntregasColaborador
            :entregas="entregas.enviados_Lider"
            :usuario="usuario"
            :tipoEntrega="tipoEntrega"
          />
        </q-tab-panel>
        <q-tab-panel name="rechazadoLider">
          <TablaEntregasColaborador
            :entregas="entregas.rechazados_Lider"
            :usuario="usuario"
            :tipoEntrega="tipoEntrega"
          />
        </q-tab-panel>
        <q-tab-panel name="enviadoUPCI">
          <TablaEntregasColaborador
            :entregas="entregas.enviados_UPCI"
            :usuario="usuario"
            :tipoEntrega="tipoEntrega"
          />
        </q-tab-panel>
        <q-tab-panel name="rechazadoUPCI">
          <TablaEntregasColaborador
            :entregas="entregas.rechazados_UPCI"
            :usuario="usuario"
            :tipoEntrega="tipoEntrega"
          />
        </q-tab-panel>
        <q-tab-panel name="finalizado">
          <TablaEntregasColaborador
            :entregas="entregas.finalizados"
            :usuario="usuario"
            :tipoEntrega="tipoEntrega"
          />
        </q-tab-panel>
      </q-tab-panels>
    </template>
  </q-splitter>
</template>
<script>
import { ref, toRef, defineComponent } from "vue";
import TablaEntregasColaborador from "src/components/TablaEntregasColaborador.vue";

export default defineComponent({
  components: {
    TablaEntregasColaborador,
  },
  props: {
    entregas: Object,
    tipoEntrega: String,
    usuario: Object,
  },
  setup(props) {
    const innerTab = ref("borrador");
    return {
      entregas: toRef(props, "entregas"),
      nombrePanel: toRef(props, "nombrePanel"),
      tipoEntrega: toRef(props, "tipoEntrega"),
      splitterModel: ref(15),
      innerTab,
    };
  },
});
</script>

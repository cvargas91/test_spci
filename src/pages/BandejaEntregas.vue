<template>
  <q-page>
    <div v-if="entrega.estadoWorkflow" class="q-pa-md">
      <q-card class="my-card bg-teal-2">
        <q-card-section horizontal>
          <q-card-section>
            <q-avatar color="white" text-color="cyan-8" icon="done" />
          </q-card-section>
          <q-card-section class="text-textoAzul">
            <div class="text-h6"><b>Gracias por Colaborar</b></div>
            Estado de la entrega actualizado
          </q-card-section>
        </q-card-section>      
        <q-card-section class="q-pt-none">
          <q-btn color="light-blue-10"
            label="Volver a la bandeja de entregas"
            @click="limpiaBandeja"
          />          
        </q-card-section>
        <q-card-section>
          <q-separator class="bg-textoAzul" inset />
        </q-card-section>
      </q-card>
    </div>
    <div v-else>
      <div class="q-pa-md" v-if="usuario.perfil">
        <q-card>
          <q-tabs
            :model-value="tab"
            @update:model-value="cambiaTab"
            dense
            class="tablaAcciones"
            active-color="primary"
            indicator-color="primary"
            align="justify"
          >
            <q-tab name="misVerificadores" class="text-textoAzul"><b>Verificadores</b></q-tab>
            <q-tab name="misProductos" class="text-textoAzul"><b>Productos</b></q-tab>
            <q-tab name="verificadoresSinMI" class="text-textoAzul"><b>Verificadores de mi equipo</b></q-tab>
            <q-tab name="productosSinMI" class="text-textoAzul"><b>Productos de mi equipo</b></q-tab>
          </q-tabs>

          <q-separator />

          <q-tab-panels v-model="tab" animated>
            <q-tab-panel
              name="misVerificadores"
              class="q-pa-none tablaAcciones"
              v-if="verificador.verificadores"
            >
              <PanelBandejaEntrega
                :entregas="verificador.verificadores"
                :usuario="usuario"
                tipoEntrega="verificador"
              />
            </q-tab-panel>
            <q-tab-panel
              name="misProductos"
              class="q-pa-none tablaAcciones"
              v-if="producto.productos"
            >
              <PanelBandejaEntrega
                :entregas="producto.productos"
                :usuario="usuario"
                tipoEntrega="producto"
              />
            </q-tab-panel>
            <q-tab-panel
              name="verificadoresSinMI"
              class="q-pa-none tablaAcciones"
              v-if="verificador.verificadores"
            >
              <PanelBandejaEntrega
                :entregas="verificador.verificadores"
                :usuario="usuario"
                tipoEntrega="verificador"
              />
            </q-tab-panel>
            <q-tab-panel
              name="productosSinMI"
              class="q-pa-none tablaAcciones"
              v-if="producto.productos"
            >
              <PanelBandejaEntrega
                :entregas="producto.productos"
                :usuario="usuario"
                tipoEntrega="producto"
              />
            </q-tab-panel>
          </q-tab-panels>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script>
import { ref, computed, onMounted, defineComponent } from "vue";
import { useStore } from "vuex";
import PanelBandejaEntrega from "src/components/PanelBandejaEntrega.vue";

export default defineComponent({
  components: {
    PanelBandejaEntrega,
  },
  setup() {
    const store = useStore();
    const usuario = computed(() => store.state.usuarix.usuario);
    const entrega = computed(() => store.state.entrega);
    const producto = computed(() => store.state.producto);
    const verificador = computed(() => store.state.verificador);
    const tab = ref("misVerificadores");
    const innerTab = ref("borrador");
    const cambiaTab = (value, event) => {
      store.dispatch("accion/limpiaAcciones");
      if (value == "misProductos") store.dispatch("producto/reqMisProductos");
      else if (value == "misVerificadores")
        store.dispatch("verificador/reqMisVerificadores");
      else if (value == "productosSinMI")
        store.dispatch("producto/reqProductosUnidad");
      else if (value == "verificadoresSinMI")
        store.dispatch("verificador/reqVerificadoresUnidad");
      tab.value = value;
      innerTab.value = "borrador";
    };
    onMounted(() => {
      store.dispatch("entrega/limpiaEntregas");
      store.dispatch("verificador/reqMisVerificadores");
    });
    return {
      usuario,
      entrega,
      opcionEntregables: ref("reqEntregablesMios"),
      producto,
      verificador,
      limpiaBandeja: () => {
        tab.value = "misProductos";
        innerTab.value = "borrador";
        store.dispatch("entrega/limpiaEntregas");
        store.dispatch("verificador/reqMisVerificadores");
      },
      cambiaTab,
      tab,
      innerTab,
    };
  },
});
</script>

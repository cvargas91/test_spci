<template>
  <q-page>
    <div class="q-pa-md" v-if="usuario.perfil">
      <div class="text-textoAzul text-h6">
        <b
          >Seleccione una acción haciendo clic en la casilla para desplegar
          opciones</b
        >
      </div>
      <div class="q-gutter-y-md">
        <q-card>
          <q-tabs
            :model-value="tab"
            @update:model-value="cambiaTab"
            dense
            class="tablaAcciones"
            active-color="primary"
            indicator-color="primary"
            align="justify"
            narrow-indicator
          >
            <q-tab
              class="text-textoAzul"
              name="Responsable"
              label="Responsable"
            />
            <q-tab 
              class="text-textoAzul" 
              name="Soporte" 
              label="Soporte" />
            <q-tab
              class="text-textoAzul"
              name="Consultado"
              label="Consultado"
            />
            <q-tab 
              class="text-textoAzul"
              name="Informado" 
              label="Informado" 
            />
          </q-tabs>
          <q-separator color="blue" inset />
          <q-tab-panels v-model="tab" animated>
            <q-tab-panel name="Responsable">
              <TablaAcciones
                :acciones="accion.acciones"
                referencia="AccionesPMI"
              />
            </q-tab-panel>
            <q-tab-panel name="Soporte">
              <TablaAcciones
                :acciones="accion.acciones"
                referencia="AccionesPMI"
              />
            </q-tab-panel>
            <q-tab-panel name="Consultado">
              <TablaAcciones
                :acciones="accion.acciones"
                referencia="AccionesPMI"
              />
            </q-tab-panel>
            <q-tab-panel name="Informado">
              <TablaAcciones
                :acciones="accion.acciones"
                referencia="AccionesPMI"
              />
            </q-tab-panel>
            
          </q-tab-panels>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script>
import { ref, computed, onMounted, onUnmounted, defineComponent } from "vue";
import { useStore } from "vuex";
import TablaAcciones from "src/components/TablaAcciones.vue";

export default defineComponent({
  components: {
    TablaAcciones,
  },
  setup() {
    const store = useStore();
    const accion = computed(() => store.state.accion);
    const tab = ref("Responsable");
    const cambiaTab = (value, event) => {
      store.dispatch("accion/limpiaAcciones");
      tab.value = value;
      store.dispatch("accion/reqAccionesPorRol", {
        rol: value,
        origen: "PMI",
      });
    };
    onMounted(() => {
      store.dispatch("accion/reqAccionesPorRol", {
        rol: tab.value,
        origen: "PMI",
      });
      store.dispatch("entrega/limpiaNuevaEntrega");
      store.dispatch("producto/limpiaNuevoProducto");
      store.dispatch("verificador/limpiaNuevoVerificador");
    });
    onUnmounted(() => {
      store.dispatch("accion/limpiaAcciones");
      store.dispatch("producto/limpiaNuevoProducto");
      store.dispatch("verificador/limpiaNuevoVerificador");
    });
    return {
      usuario: computed(() => store.state.usuarix.usuario),
      accion,
      tab,
      cambiaTab,
    };
  },
});
</script>

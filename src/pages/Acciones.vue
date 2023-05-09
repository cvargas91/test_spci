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
              label="Soporte" 
            />
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
          <q-tab-panels v-model="tab" animated v-if="accion.acciones.length">          
            <q-tab-panel name="Responsable">
              <OpcionOrigenAccion
                :acciones="accion.acciones"
                referencia="AccionesPOA"
              />
            </q-tab-panel>
            <q-tab-panel name="Soporte">
              <OpcionOrigenAccion
                :acciones="accion.acciones"
                referencia="AccionesPOA"
              />
            </q-tab-panel>
            <q-tab-panel name="Consultado">
              <OpcionOrigenAccion
                :acciones="accion.acciones"
                referencia="AccionesPOA"
              />
            </q-tab-panel>
            <q-tab-panel name="Informado">
              <OpcionOrigenAccion
                :acciones="accion.acciones"
                referencia="AccionesPOA"
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
import OpcionOrigenAccion from "src/components/OpcionOrigenAccion.vue";

export default defineComponent({
  components: {
    TablaAcciones,
    OpcionOrigenAccion,
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
        origen: "POA",
      });
    };
    onMounted(() => {
      store.dispatch("accion/reqAccionesPorRol", {
        rol: tab.value,
        origen: "POA",
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

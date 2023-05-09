<template>
  <div class="q-pa-md">
    <PopupCancelarNuevaEntrega
      :mostrar="mostrarPopupCancelar"
      @update:mostrar="mostrarPopupCancelar = $event"
      @respuestaPopup="handlerPopupCancelar"
    />
    <!--estado entrega una vez actualizado-->
    <div v-if="verificador.verificadorEditado">
      <div class="text-h6">¡Felicitaciones!</div>
      <p>Se ha actualizado el Verificador</p>
      <q-btn
        label="Ir a la bandeja de entregas"
        to="bandejaEntregas"
        color="primary"
      />
    </div>
    <div v-else-if="entrega.aModificar">
      <div class="text-h6">
        Actualizando {{ entrega.aModificar.entrega.descripcion }}
      </div>
      <q-stepper
        v-model="step"
        ref="stepper"
        color="blue"
        animated
        header-class="tablaAcciones"
      >
        <q-step :name="1" title="Indicador" icon="settings" :done="step > 1">
          <!--class="tarjetaAmarilla"-->
          <div class="text-h6">
            Seleccione un verificador de las siguientes funciones de
            {{ entrega.aModificar.entrega.indicador.funcion.accion.id_uaysen }}
          </div>
          <div class="text-subtitle1">
            {{ entrega.aModificar.entrega.indicador.funcion.accion.titulo }}
          </div>
          <div class="text-subtitle2">
            Objetivo:
            {{ entrega.aModificar.entrega.indicador.funcion.accion.objetivo }}
          </div>
          <div class="row" v-for="item in accion.funciones" :key="item.id">
            <div class="col">
              <q-card>
                <!--class="tarjetaAmarilla"-->
                <q-card-section class="q-pa-sm">
                  <div class="text-body1">
                    {{ item.nombre }}
                  </div>
                </q-card-section>
                <q-card-actions vertical>
                  <div v-if="item.indicador_set.length" class="column">
                    <q-btn-toggle
                      no-caps
                      align="left"
                      class="col"
                      v-for="subItem in item.indicador_set"
                      :key="subItem.id"
                      v-model="indicadorSeleccionado"
                      toggle-color="primary"
                      :options="[{ label: subItem.nombre, value: subItem }]"
                    />
                  </div>
                  <div v-else="item.indicador_set.length" class="bg-accent">
                    No hay indicadores definidos para esta función. Por favor,
                    notificar este incidente a UPCI para ser revisado. Gracias
                  </div>
                </q-card-actions>
              </q-card>
            </div>
          </div>
        </q-step>
        <q-step :name="2" title="Detalles" icon="assignment" :done="step > 2">
          <!--class="tarjetaAmarilla"-->
          <div class="row">
            <div class="col-4 q-ma-sm">
              <q-card flat bordered>
                <!--class="tarjetaAmarilla"-->
                <q-card-section>
                  <div class="text-h6">
                    {{ indicadorSeleccionado.nombre }}
                  </div>
                </q-card-section>
                <q-separator inset />
                <q-card-section class="q-pt-none">
                  <div class="text-weight-bold">Fórmula</div>
                  {{ indicadorSeleccionado.formula }}
                </q-card-section>
                <q-card-section class="q-pt-none">
                  <div class="text-weight-bold">Meta</div>
                  <div>
                    actualmente:
                    {{ entrega.aModificar.valor }}
                  </div>
                  {{ indicadorSeleccionado.meta }}
                </q-card-section>
                <q-card-section class="q-pt-none">
                  <div class="text-weight-bold">Verificador</div>
                  {{ indicadorSeleccionado.nombreVerificador }}
                </q-card-section>
              </q-card>
            </div>
            <div class="col q-ma-sm">
              <q-card flat bordered>
                <!--class="tarjetaAmarilla"-->
                <q-card-section>
                  <div class="text-h6">Indique el avance del indicador</div>
                </q-card-section>
                <q-separator inset />
                <q-form class="q-gutter-md">
                  <q-card-section class="q-pt-none">
                    <q-input
                      filled
                      v-model="verificadorValor"
                      :label="indicadorSeleccionado.formula"
                      hint="Valor del indicador al día de hoy"
                      lazy-rules
                      :rules="[
                        (val) =>
                          (val && val.length > 0) || 'Debe ingresar un valor',
                      ]"
                    />
                  </q-card-section>
                  <q-card-section class="q-pt-none">
                    <q-input
                      type="textarea"
                      filled
                      v-model="verificadorDescripcion"
                      label="Descripción o comentarios sobre valor indicado"
                      lazy-rules
                      :rules="[
                        (val) =>
                          (val && val.length > 0) ||
                          'Debe ingresar una descripción o comentario',
                      ]"
                    >
                      <template v-if="verificadorDescripcion" v-slot:append />
                    </q-input>
                  </q-card-section>
                </q-form>
              </q-card>
            </div>
          </div>
        </q-step>
        <q-step :name="3" title="Adjunta" icon="create_new_folder">
          <!--class="tarjetaAmarilla"-->
          <div class="text-h6">Adjuntar el verificador</div>
          <p>
            Adjunta documentos que necesites para demostrar el avance del
            indicador. Éstos quedarán almacenados en Google Drive y serán
            revisados por tu jefatura y el equipo de UPCI
          </p>
          <div class="text-weight-bold">
            Documentos actuales en Google Drive:
          </div>
          <div v-if="entrega.adjuntosEdicionEntrega">
            <q-list
              v-for="item in entrega.adjuntosEdicionEntrega"
              :key="item.id"
              bordered
              class="rounded-borders"
              style="max-width: 600px"
            >
              <q-item>
                <q-item-section top class="col-2 gt-sm">
                  <q-item-label class="q-mt-sm"> {{ item.name }} </q-item-label>
                  <q-item-section top side align="right">
                    <div class="text-grey-8 q-gutter-xs">
                      <q-btn
                        class="gt-xs"
                        size="12px"
                        flat
                        dense
                        round
                        icon="delete"
                        @click="eliminarAdjunto(item)"
                      />
                      <q-btn
                        type="a"
                        target="_blank"
                        :href="item.downloadUrl"
                        class="gt-xs"
                        size="12px"
                        flat
                        dense
                        round
                        icon="download"
                      />
                    </div>
                  </q-item-section>
                </q-item-section>
              </q-item>
            </q-list>
          </div>
  
          <q-separator color="blue" inset />

          <Picker :baseDir="indicadorSeleccionado.dirGoogle" />
        </q-step>
        <template v-slot:navigation>
          <q-stepper-navigation>
            <!--class="tarjetaAmarilla"-->
            <q-btn
              v-if="step == 1"
              @click="$refs.stepper.next()"
              color="btnContinuar"
              label="Continuar"
              :disable="!indicadorSeleccionado"
            />
            <q-btn
              v-if="step == 2"
              @click="$refs.stepper.next()"
              color="btnContinuar"
              label="Continuar"
              :disable="!verificadorValor || !verificadorDescripcion"
            />
            <q-btn
              v-if="step == 3"
              @click="submitEdicionVerificador"
              color="primary"
              label="Finalizar"
              :disable="!entrega.adjuntosEdicionEntrega"
            />
            <q-btn
              v-if="step > 1"
              flat
              color="btnVolver"
              @click="$refs.stepper.previous()"
              label="Volver"
              class="q-ml-sm"
            />
            <q-btn
              color="btnCancelar"
              label="Cancelar"
              class="q-ml-sm"
              @click="clicCancelar"
            />
          </q-stepper-navigation>
        </template>
      </q-stepper>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import Picker from "src/components/Picker.vue";
import PopupCancelarNuevaEntrega from "src/components/PopupCancelarNuevaEntrega.vue";

export default {
  components: {
    Picker,
    PopupCancelarNuevaEntrega,
  },

  setup() {
    const router = useRouter();
    const store = useStore();
    const entrega = computed(() => store.state.entrega);
    const verificador = computed(() => store.state.verificador);
    const accion = computed(() => store.state.accion);
    const usuario = computed(() => store.state.usuarix);
    const mostrarPopupCancelar = ref(false);
    const respuestaPopupCancelar = ref("");
    const indicadorSeleccionado = ref(
      entrega.value.aModificar.entrega.indicador
    );
    const verificadorValor = ref(entrega.value.aModificar.entrega.valor);
    const verificadorDescripcion = ref(
      entrega.value.aModificar.entrega.descripcion
    );
    const adjuntosActuales = entrega.value.aModificar.entrega.adjuntos;
  
    const clickAdjunto = (item) => {
      window.open(item.url);
    };
    const submitEdicionVerificador= () => {
        const verificadorModificado = {
          id: entrega.value.aModificar.entrega.id,
          usuario: usuario.value.usuario.id,
          indicador: indicadorSeleccionado.value.id,
          valor: verificadorValor.value,
          descripcion: verificadorDescripcion.value,
          adjuntos: entrega.value.adjuntosEdicionEntrega,
        };
        
        
        store.dispatch("entrega/setModificaVerificador", verificadorModificado);
        router.push("bandejaEntregas");
    };
        
    onMounted(() => {
      store.dispatch("entrega/limpiaAdjuntosEdicion");
      if (entrega.value.aModificar) {
        store.dispatch(
          "accion/reqFuncionesPorAccion",
          entrega.value.aModificar.entrega.indicador.funcion.accion.id
        );
        if(adjuntosActuales){
          store.dispatch("entrega/setAdjuntosEdicionEntrega", adjuntosActuales);
        } else{
          console.log("Entrega sin adjuntos");
        }
      }
    });
    return {
      clickAdjunto,
      verificador,
      entrega,
      accion,
      indicadorSeleccionado: ref(),
      verificadorValor,
      verificadorDescripcion,
      mostrarPopupCancelar,
      respuestaPopupCancelar,
      eliminarAdjunto(item) {
        store.dispatch("entrega/setAdjuntosEdicionEntrega", [item]);
      },
      
      step: ref(1),
      handlerPopupCancelar: (respuesta) => {
        mostrarPopupCancelar.value = false;
        if (respuesta == "guarda") {
          submitEdicionVerificador();
          router.push("bandejaEntregas");
        } else if (respuesta == "sale") {
          router.push("bandejaEntregas");
        } else {
          // se hace nada
        }
      },
      submitEdicionVerificador,
      clicCancelar: () => {      
        mostrarPopupCancelar.value = true;
      },
    };
  },
};
</script>

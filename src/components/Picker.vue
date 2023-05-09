<template>
  <div v-if="token">
    <q-btn
      color="btnAdjuntar"
      icon="attach_file"
      label="Adjuntar documentos"
      @click="driveIconClicked()"
    />
  </div>
  <div v-else class="text-h6">Un momento por favor...</div>
</template>
<script>
import { computed, onBeforeMount, onMounted, onUnmounted } from "vue";
import { useStore } from "vuex";

export default {
  props: {
    baseDir: String,
  },
  setup(props) {
    const store = useStore();
    const token = computed(() => store.state.usuarix.token);
    const entrega = computed(() => store.state.entrega);
    var gDrive = document.createElement("script");
    var pickerApiLoaded = false;
    const developerKey = "AIzaSyDakTEUxGmv1YzAmFOY_a_TjLbHi0AInBQ";
    //const developerKey = "AIzaSyBGoyLW_Zq1QK6EWh6jkLcEDlsqI5XTc6s";
    onMounted(() => {
      store.dispatch("usuarix/reqAccessToken");
      gDrive = document.createElement("script");
      gDrive.setAttribute("type", "text/javascript");
      gDrive.setAttribute("src", "https://apis.google.com/js/api.js");
      document.head.appendChild(gDrive);
    });
    onUnmounted(() => {
      gDrive.remove();
    });
    const driveIconClicked = async function () {
      gapi.load("picker", () => {
        pickerApiLoaded = true;
        createPicker();
      });
    };
    // Create and render a Picker object for picking user Photos.
    const createPicker = function () {
      if (pickerApiLoaded && token) {
        var view = new google.picker.View(google.picker.ViewId.DOCS).setParent(
          props.baseDir
        );
        var uploadView = new google.picker.DocsUploadView().setParent(props.baseDir);
        var picker = new google.picker.PickerBuilder()
          .setLocale("es-419")
          .enableFeature(google.picker.Feature.MULTISELECT_ENABLED)
          // descomentar la siguiente linea para ver los archivos
          //.addView(view)
          .addView(uploadView)
          .setOAuthToken(token.value)
          .setDeveloperKey(developerKey)
          .setCallback(pickerCallback)
          .build();
        picker.setVisible(true);
      }
    };
    const pickerCallback = async function (data) {
      var url = "";
      var name = "";

      if (data[google.picker.Response.ACTION] === google.picker.Action.PICKED) {
        if (entrega.value.aModificar) {
          store.dispatch("entrega/setAdjuntosEdicionEntrega", data.docs);
        } else {
          store.dispatch("entrega/setAdjuntosNuevaEntrega", data.docs);
        }
        //store.dispatch("entrega/setAdjuntosNuevaEntrega", data.docs);
      }
      pickerApiLoaded = false;
    };
    return {
      driveIconClicked: driveIconClicked,
      createPicker: createPicker,
      pickerCallback: pickerCallback,
      token: token,
    };
  },
};
</script>

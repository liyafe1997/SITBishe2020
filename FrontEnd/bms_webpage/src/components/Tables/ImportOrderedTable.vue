<template>
  <div>
    <md-table v-model="itemdata" :table-header-color="tableHeaderColor">
      <md-table-row slot="md-table-row" slot-scope="{ item }">
        <md-table-cell md-label="ID">{{ item.id }}</md-table-cell>
        <md-table-cell md-label="名称">{{ item.name }}</md-table-cell>
        <md-table-cell md-label="数量">{{ item.number }}</md-table-cell>
        <md-table-cell md-label="货源">{{ item.factory }}</md-table-cell>
      </md-table-row>
    </md-table>
  </div>
</template>

<script>
import { StatsCard, SaleOrderedTable } from "@/components";
import Cookies from "js-cookie";
import Vue from "vue";
import VueResource from "vue-resource";
Vue.use(VueResource);
export default {
  name: "import-ordered-table",
  props: {
    tableHeaderColor: {
      type: String,
      default: ""
    }
  },
  data() {
    return {
      selected: [],
      itemdata: []
    };
  },
  mounted() {
    /*
    Vue.http.get("/checklogin").then(
      function(res) {
        if (res.status != 200) {
          window.location.href = "/index.html";
        }
      },
      function() {
        //document.write("Back-End");
      }
    ),*/
    this.getData();
  },
  methods: {
    getData() {
      Vue.http.get("/get_sorted_import_data").then(response => {
        this.itemdata = response.body;
      });
    }
  }
};
</script>

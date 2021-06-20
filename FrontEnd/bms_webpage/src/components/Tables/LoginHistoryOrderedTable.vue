<template>
  <div>
    <md-table v-model="tabledata" :table-header-color="tableHeaderColor">
      <md-table-row slot="md-table-row" slot-scope="{ item }">
        <md-table-cell md-label="UID">{{ item.uid }}</md-table-cell>
        <md-table-cell md-label="用户名">{{ item.username }}</md-table-cell>
        <md-table-cell md-label="时间">{{ item.time }}</md-table-cell>
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
  name: "",
  props: {
    tableHeaderColor: {
      type: String,
      default: ""
    }
  },
  data() {
    return {
      selected: [],
      itemdata: [],
      tabledata: [],
      usernamedict: new Object()
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
      Vue.http.get("/get_login_history").then(response => {
        this.itemdata = response.body;
        for (var p in this.itemdata) {
          window.console.log(p);
          let dateobj = new Date(Number(this.itemdata[p].time + "000"));
          this.itemdata[p].time =
            dateobj.getFullYear() +
            "-" +
            dateobj.getMonth() +
            "-" +
            dateobj.getDate() +
            " " +
            dateobj.getHours() +
            ":" +
            dateobj.getMinutes() +
            ":" +
            dateobj.getSeconds();
        }

        Vue.http.get("/get_all_username", {}).then(response => {
          window.console.log(p);
          this.allusername = response.body;

          for (let i in this.allusername) {
            this.usernamedict[
              Number(this.allusername[i].id)
            ] = this.allusername[i].username;
          }
          for (let p in this.itemdata) {
            this.itemdata[p].username = this.usernamedict[
              Number(this.itemdata[p].uid)
            ];
          }
          this.tabledata = this.itemdata;
        });
      });
    }
  }
};
</script>


<template>
  <div>
    <md-dialog style="z-index: 8" :md-active.sync="modifydialog.show">
      <md-dialog-title>
        入库商品
        <small>（ID:{{modifydialog.itemdata.id}}）</small>
      </md-dialog-title>

      <div style="padding:20px;">
        <md-field>
          <label>入库数量</label>
          <md-input v-model="modifydialog.tostorenumber" type="number"></md-input>
        </md-field>

        <md-autocomplete
          v-model="modifydialog.tostoreplace"
          :md-options="store_places"
        >
          <label>存入仓库</label>
        </md-autocomplete>

        <br />
        <small>对仓库中已存在的商品将增加库存数据数量</small>
        <br />
        <small>如仓库中不存在，则自动新增一条记录</small>
      </div>
      <md-dialog-actions>
        <md-button class="md-primary" @click="modifydialog.show = false">取消</md-button>
        <md-button class="md-primary" @click="confirmImportItem">确定</md-button>
      </md-dialog-actions>
    </md-dialog>

    <md-dialog-alert style="z-index: 100" :md-active.sync="popupdialog" :md-content="dialogcontent" md-confirm-text="好" />

    <md-table v-model="import_items" :table-header-color="tableHeaderColor">
      <md-table-row slot="md-table-row" slot-scope="{ item }">
        <md-table-cell md-label="ID">{{ item.id }}</md-table-cell>
        <md-table-cell md-label="商品名">{{ item.name }}</md-table-cell>
        <md-table-cell md-label="数量">{{ item.number }}</md-table-cell>
        <md-table-cell md-label="货源">{{ item.factory }}</md-table-cell>
        <md-table-cell md-label="操作">
          <md-button
            class="md-raised md-success"
            v-bind:itemid="item.id"
            v-on:click="tostoreitem($event)"
          >入库</md-button>
        </md-table-cell>
      </md-table-row>
    </md-table>
  </div>
</template>
<script>
import Cookies from "js-cookie";
import Vue from "vue";
import VueResource from "vue-resource";
Vue.use(VueResource);
export default {
  name: "store-from-import-table",
  props: {
    tableHeaderColor: {
      type: String,
      default: ""
    }
  },
  data: function() {
    return {
      dialogcontent: "",
      popupdialog: false,

      modifydialog: {
        show: false,
        itemdata: {}
      },

      selected: [],
      currentusername: "",
      import_items: []
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
      Vue.http.get("/get_all_import_finished_item").then(response => {
        this.import_items = response.body;
      });
      Vue.http.get("/get_all_store_places").then(response => {
        this.store_places = response.body;
      });
    },
    tostoreitem: function(e) {
      var itemid = e.currentTarget.getAttribute("itemid");
      this.modifydialog.itemdata.id = itemid;
      this.modifydialog.show = true;
    },

    confirmImportItem() {
      Vue.http
        .get("/store_from_import", {
          params: {
            id: this.modifydialog.itemdata.id,
            number: this.modifydialog.tostorenumber,
            storeplace: this.modifydialog.tostoreplace
          }
        })
        .then(response => {
          window.console.log(response.body);
          this.users_items = response.body;
          if (response.body == "-3") {
            this.dialogcontent = "错误：进货库中无此商品";
            this.popupdialog = true;
          } else if (response.body == "-2") {
            this.dialogcontent = "错误：进货单中的数量小于入库数量";
            this.popupdialog = true;
          } else if (response.body == "-1") {
            this.dialogcontent = "数据库错误：更新进货单商品数量失败";
            this.popupdialog = true;
          } else if (response.body == "-4") {
            this.dialogcontent = "数据库错误：更新库存商品失败";
            this.popupdialog = true;
          } else if (response.body == "1") {
            this.dialogcontent = "入库成功（已有库存商品增加库存数量）";
            this.popupdialog = true;
          } else if (response.body == "0") {
            this.dialogcontent = "入库成功（新库存商品）";
            this.popupdialog = true;
          } else if (response.body == "-5") {
            this.dialogcontent = "数据库错误：新增库存商品失败";
            this.popupdialog = true;
          }
        });
      this.getData();
    }
  },
  watch: {
    popupdialog: {
      handler(newName, oldName) {
        if (newName == false) {
          window.location.reload();
        }
      }
    }
  }
};
</script>

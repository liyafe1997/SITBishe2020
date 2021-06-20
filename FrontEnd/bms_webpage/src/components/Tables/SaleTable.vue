<template>
  <div>
    <div>
      <md-dialog :md-active.sync="modifydialog.show">
        <md-dialog-title>修改商品(ID={{modifydialog.itemdata.id}})</md-dialog-title>

        <div style="padding:20px;">
          <md-field>
            <label>名称</label>
            <md-input v-model="modifydialog.itemdata.name"></md-input>
          </md-field>
          <md-field>
            <label>数量</label>
            <md-input v-model="modifydialog.itemdata.number" type="number"></md-input>
          </md-field>
          <md-field>
            <label>客户</label>
            <md-input v-model="modifydialog.itemdata.custom"></md-input>
          </md-field>
          <md-field>
            <label>状态</label>
            <md-select v-model="modifydialog.itemdata.finished">
              <md-option value="0">未完成</md-option>
              <md-option value="1">已完成</md-option>
            </md-select>
          </md-field>
        </div>
        <md-dialog-actions>
          <md-button class="md-primary" @click="modifydialog.show = false">取消</md-button>
          <md-button class="md-primary" @click="confirmModifyItem">确定</md-button>
        </md-dialog-actions>
      </md-dialog>
    </div>
    <md-dialog-alert :md-active.sync="popupdialog" :md-content="dialogcontent" md-confirm-text="好" />

    <md-dialog-confirm
      :md-active.sync="confirmdialog"
      md-title="删除商品"
      md-content="确定要删除该商品吗?"
      md-confirm-text="确定"
      md-cancel-text="取消"
      @md-confirm="confirmDeleteItem"
    />

    <md-dialog-confirm
      :md-active.sync="confirmfinishdialog"
      md-title="完成订单"
      md-content="确定要将该订单标记为已完成吗?"
      md-confirm-text="确定"
      md-cancel-text="取消"
      @md-confirm="confirmFinishItem"
    />

    <md-table v-model="sale_items" :table-header-color="tableHeaderColor">
      <md-table-row slot="md-table-row" slot-scope="{ item }">
        <md-table-cell md-label="ID">{{ item.id }}</md-table-cell>
        <md-table-cell md-label="商品名">{{ item.name }}</md-table-cell>
        <md-table-cell md-label="数量">{{ item.number }}</md-table-cell>
        <md-table-cell md-label="客户">{{ item.custom }}</md-table-cell>
        <md-table-cell md-label="状态">
          <p v-if="item.finished==0 ? true : false">未完成</p>
          <p v-if="item.finished==1 ? true : false">已完成</p>
        </md-table-cell>
        <md-table-cell md-label="操作">
          <md-button
            v-bind:itemid="item.id"
            v-on:click="deleteitem($event)"
            v-if="role==5 ? false : true"
          >删除</md-button>
          <md-button
            v-bind:itemid="item.id"
            v-bind:itemname="item.name"
            v-bind:itemnumber="item.number"
            v-bind:itemcustom="item.custom"
            v-bind:itemfinished="item.finished"
            v-on:click="modifyitem($event)" v-if="role==5 ? false : true"
            class="md-primary"
          >修改</md-button>
          <md-button
            v-if="item.finished==0 ? true : false"
            class="md-success"
            v-bind:itemid="item.id"
            v-on:click="finishitem($event)"
          >标记为完成</md-button>
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
  name: "sale-table",
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
      deleteitemid: 0,
      confirmdialog: false,
      confirmfinishdialog: false,
      modifydialog: {
        show: false,
        itemdata: {}
      },

      selected: [],
      currentusername: "",
      sale_items: [],
      role: Cookies.get("role")
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
      Vue.http.get("/get_all_sale_item").then(response => {
        this.sale_items = response.body;
      });
    },
    deleteitem: function(e) {
      var itemid = e.currentTarget.getAttribute("itemid");
      this.deleteitemid = itemid;
      this.confirmdialog = true;
    },
    finishitem: function(e) {
      var itemid = e.currentTarget.getAttribute("itemid");
      this.finishitemid = itemid;
      this.confirmfinishdialog = true;
    },
    confirmFinishItem: function(e) {
      Vue.http
        .get("/mark_sale_item_finished", { params: { id: this.finishitemid } })
        .then(response => {
          if (response.body == "ok") {
            this.dialogcontent = "操作成功";
            this.popupdialog = true;
            this.getData();
          } else {
            this.dialogcontent = "操作失败";
            this.popupdialog = true;
          }
        });
    },
    modifyitem: function(e) {
      this.modifydialog.itemdata.id = e.currentTarget.getAttribute("itemid");
      this.modifydialog.itemdata.name = e.currentTarget.getAttribute(
        "itemname"
      );
      this.modifydialog.itemdata.number = e.currentTarget.getAttribute(
        "itemnumber"
      );
      this.modifydialog.itemdata.custom = e.currentTarget.getAttribute(
        "itemcustom"
      );
      this.modifydialog.itemdata.finished = e.currentTarget.getAttribute(
        "itemfinished"
      );
      this.modifydialog.show = true;
      window.console.log(this.modifydialog.itemdata);
    },
    confirmModifyItem() {
      Vue.http
        .get("/update_sale_item_by_id", {
          params: {
            id: this.modifydialog.itemdata.id,
            name: this.modifydialog.itemdata.name,
            number: this.modifydialog.itemdata.number,
            custom: this.modifydialog.itemdata.custom,
            finished: this.modifydialog.itemdata.finished
          }
        })
        .then(response => {
          window.console.log(response.body);
          this.users_items = response.body;
          if (response.body == "ok") {
            this.modifydialog.show = false;
            this.dialogcontent = "修改成功";
            this.popupdialog = true;
            this.getData();
          } else {
            this.modifydialog.show = false;
            this.dialogcontent = "修改失败";
            this.popupdialog = true;
          }
        });
      this.modifydialog.show = false;
    },

    confirmDeleteItem() {
      Vue.http
        .get("/delete_sale_item_by_id", { params: { id: this.deleteitemid } })
        .then(response => {
          window.console.log(response.body);
          this.users_items = response.body;
          if (response.body == "ok") {
            this.dialogcontent = "删除成功";
            this.popupdialog = true;
            this.getData();
          } else {
            this.dialogcontent = "删除失败";
            this.popupdialog = true;
          }
        });
    }
  },
  watch: {
    modifydialog: {
      handler(newName, oldName) {
        if (newName == false) {
          this.dialogDismiss();
        }
      }
    }
  }
};
</script>

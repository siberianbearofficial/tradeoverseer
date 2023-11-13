import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {OrderModel} from "../models/order-model";

const BASE_API_URL: string = '/api';
const ORDERS_URL: string = 'orders';

@Injectable({
  providedIn: 'root'
})
export class OrderApiService {

  constructor(private http: HttpClient) {
  }

  public sendOrder(order: OrderModel) {
    return this.http.post(`${BASE_API_URL}/${ORDERS_URL}`, order);
  }
}

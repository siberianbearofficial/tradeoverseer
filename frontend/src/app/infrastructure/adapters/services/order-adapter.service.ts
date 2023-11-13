import {Injectable} from '@angular/core';
import {Order} from "../../../core/domain/entities/order";
import {OrderModel} from "../../models/order-model";
import {OrderApiService} from "../../api/order-api.service";
import {map, Observable} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class OrderAdapterService {

  constructor(private orderApi: OrderApiService) {
  }

  public sendOrder(order: Order): Observable<void> {
    return this.orderApi.sendOrder(order as OrderModel).pipe(map(() => void 0));
  }
}

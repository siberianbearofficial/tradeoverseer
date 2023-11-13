import {Observable} from "rxjs";
import {Order} from "../../entities/order";

export interface OrderServiceInterface {
  sendOrder: (config: Order) => Observable<void>;
}

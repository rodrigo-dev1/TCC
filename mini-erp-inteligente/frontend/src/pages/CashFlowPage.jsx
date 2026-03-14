import CrudPage from './CrudPage'

export default function CashFlowPage() {
  return <CrudPage title="Fluxo de Caixa" endpoint="/cash-transactions" fields={[['type','Tipo(income/expense)'],['category','Categoria'],['description','Descrição'],['amount','Valor'],['transaction_date','Data ISO (opcional)']]} />
}

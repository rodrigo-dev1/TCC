import CrudPage from './CrudPage'

export default function ProductsPage() {
  return <CrudPage title="Produtos e Serviços" endpoint="/products" fields={[['name','Nome'],['description','Descrição'],['type','Tipo(product/service)'],['price','Preço'],['stock_quantity','Estoque'],['active','Ativo(true/false)']]} />
}

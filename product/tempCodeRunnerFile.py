
class ProductFilter:
    
    def __init__(self,queryset=None) -> None:
        
        self.queryset = queryset
        
    def get_queryset(self):
        return self.queryset
    
    def get_filtered_products(self,data={}):
        data = {}
        if data
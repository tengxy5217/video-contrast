from .attention import *
from .convlstm import *


class OnewayH1SPPS(nn.Module):
    def __init__(self, input_dim, hidden_dim, kernel_size, num_layers,
                 batch_first=False, bias=True, return_all_layers=False):
        super(OnewayH1SPPS, self).__init__()
        self.S = 1
        self.db_convlstm1 = Cascade2ConvLSTM(input_dim=input_dim, hidden_dim=hidden_dim, kernel_size=kernel_size,
                                             num_layers=num_layers, batch_first=False, bias=True,
                                             return_all_layers=False)
        self.db_convlstm2 = Cascade2ConvLSTM(input_dim=hidden_dim, hidden_dim=hidden_dim, kernel_size=kernel_size,
                                             num_layers=num_layers, batch_first=False, bias=True,
                                             return_all_layers=False)
        self.att = SelfAttention(input_size=hidden_dim, output_size=hidden_dim)
        self.fc = nn.Linear(hidden_dim, 2)

    def forward(self, x):
        h1, _ = self.db_convlstm1(x)
        h2, _ = self.db_convlstm2(h1)

        att_score, att_weights_ = self.att(h2)

        out_lay = h1 + self.S * att_score
        p = torch.sigmoid(self.fc(out_lay))

        return p, out_lay, att_score


class OnewayH2SPPS(nn.Module):
    def __init__(self, input_dim, hidden_dim, kernel_size, num_layers,
                 batch_first=False, bias=True, return_all_layers=False):
        super(OnewayH2SPPS, self).__init__()
        self.S = 1
        self.db_convlstm1 = Cascade2ConvLSTM(input_dim=input_dim, hidden_dim=hidden_dim, kernel_size=kernel_size,
                                             num_layers=num_layers, batch_first=False, bias=True,
                                             return_all_layers=False)
        self.db_convlstm2 = Cascade2ConvLSTM(input_dim=hidden_dim, hidden_dim=hidden_dim, kernel_size=kernel_size,
                                             num_layers=num_layers, batch_first=False, bias=True,
                                             return_all_layers=False)
        self.att = SelfAttention(input_size=hidden_dim, output_size=hidden_dim)
        self.fc = nn.Linear(hidden_dim, 2)

    def forward(self, x):
        h1, _ = self.db_convlstm1(x)
        h2, _ = self.db_convlstm2(h1)

        att_score, att_weights_ = self.att(h2)

        out_lay = att_score + h2
        p = torch.sigmoid(self.fc(out_lay))

        return p, out_lay, att_score


class OnewaySPPS(nn.Module):
    def __init__(self, input_dim, hidden_dim, kernel_size, num_layers,
                 batch_first=False, bias=True, return_all_layers=False):
        super(OnewaySPPS, self).__init__()
        self.S = 1
        self.db_convlstm1 = Cascade2ConvLSTM(input_dim=input_dim, hidden_dim=hidden_dim, kernel_size=kernel_size,
                                             num_layers=num_layers, batch_first=False, bias=True,
                                             return_all_layers=False)
        self.db_convlstm2 = Cascade2ConvLSTM(input_dim=hidden_dim, hidden_dim=hidden_dim, kernel_size=kernel_size,
                                             num_layers=num_layers, batch_first=False, bias=True,
                                             return_all_layers=False)
        self.att = SelfAttention(input_size=hidden_dim, output_size=hidden_dim)
        self.fc = nn.Linear(hidden_dim, 2)

    def forward(self, x):
        h1, _ = self.db_convlstm1(x)
        h2, _ = self.db_convlstm2(h1)

        att_score, att_weights_ = self.att(h2)

        p = torch.sigmoid(self.fc(att_score))

        return p, att_weights_, att_score